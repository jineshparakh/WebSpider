import requests
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
import time
import numpy as np
from nltk.corpus import stopwords
from collections import Counter
from nltk import word_tokenize
from nltk.util import ngrams

blacklist = ['[document]', 'noscript', 'header',
             'html', 'meta', 'head', 'script', 'style']

def getLinksFromSoup(baseURL, soup):
    def getLink(e):
        link = e["href"]
        if len(link) < 1:
            return ''
        if link.startswith('//'):
            return 'http:'+link
        if link.startswith('?'):
            if baseURL.endswith('/'):
                return baseURL[:-1]+link
            else:
                return baseURL+link
        if link[0] == '/':
            if baseURL.endswith(link):
                return ''
            if baseURL[-1] != '/':
                return baseURL+link
            else:
                return baseURL+link[1:]
        elif link[0] == '#':
            return ''
        elif len(link) > 7:
            return link
        else:
            return ''
    allLinks = list(map(getLink, soup.find_all('a', href=True)))
    allLinks = [link for link in allLinks if link]
    return list(set(allLinks))


def getWordsFromSoup(soup):
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.find_all(text=True)
    output = ''
    outputSentences = []
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
            outputSentences.append('{} '.format(t))
    outputSentences = [i.strip() for i in outputSentences]
    outputSentences = [re.sub('[^a-zA-Z0-9]+', ' ', _)
                       for _ in outputSentences]
    outputSentences = [' '.join(s for s in i.split() if not any(
        c.isdigit() for c in s)) for i in outputSentences]
    outputSentences = [i for i in outputSentences if i]
    outputSentences = [nltk.tokenize.sent_tokenize(i) for i in outputSentences]
    words = list(output.split(' '))
    words = [re.sub('[^a-zA-Z0-9]+', ' ', _) for _ in words]
    allWords = []
    for word in words:
        if len(word) > 1:
            wordsInCurrent = word.split(' ')
            for w in wordsInCurrent:
                if len(w) > 1 and not(w.isdecimal()):
                    allWords.append(w.lower())
    return allWords, outputSentences


def getBigrams(allSentences):
    allBiagrams = []
    for sentencesPerLevel in allSentences:
        bigram = []
        for sentence in sentencesPerLevel:
            token = nltk.word_tokenize(sentence)
            token = [word.lower()
                     for word in token if word not in stopwords.words('english')]
            bi = list(ngrams(token, 2))
            [bigram.append(i[0]+" " + i[1]) for i in bi if i]
        [allBiagrams.append(i) for i in bigram]
    # print(allBiagrams)
    bigrams = {}
    for i in allBiagrams:
        bigrams[i] = bigrams.get(i, 0) + 1
    b = Counter(bigrams)
    return b.most_common()


def analyzeWords(allWords):
    level = 1
    words = {}
    countOfWordsPerLevel = []
    averageLengthOfWordsPerLevel = []
    for wordsPerLevel in allWords:
        countOfWordsPerLevel.append(["Level "+str(level), len(wordsPerLevel)])
        averageLengthOfWordsPerLevel.append(
            ["Level "+str(level), sum(len(s) for s in wordsPerLevel)/len(wordsPerLevel)])
        level += 1
        filtered_words = [
            word for word in wordsPerLevel if word not in stopwords.words('english')]
        count = {}
        for i in filtered_words:
            count[i] = count.get(i, 0) + 1
            words[i] = words.get(i, 0)+1
        c = Counter(count)
    w = Counter(words)
    return w.most_common(), countOfWordsPerLevel, averageLengthOfWordsPerLevel


def startScraping(baseURL, maxLevels):
    visited = {}
    allURLs = []
    allWords = []
    allSentences = []
    for level in range(0, maxLevels+1):
        if level == 0:
            visited[baseURL] = 1
            response = requests.get(baseURL)
            html_page = response.text
            soup = BeautifulSoup(html_page, 'lxml')

            if response.status_code != 404:
                links = getLinksFromSoup(baseURL, soup)
                words, sentences = getWordsFromSoup(soup)
                allWords.append(words)
                s = []
                for sentence in sentences:
                    s.append(sentence[0])
                allSentences.append(list(s))
                allURLs.append(baseURL.split())
                allURLs.append(links)
        elif level == maxLevels:
            wordsInCurrentLevel = np.array([])
            sentencesInCurrentLevel = np.array([])
            for link in allURLs[-1]:
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    response = requests.get(link)
                    html_page = response.text
                    soup = BeautifulSoup(html_page, 'lxml')
                    words, sentences = getWordsFromSoup(soup)
                    sentencesInCurrentLevel = np.append(
                        sentencesInCurrentLevel, sentences)
                    wordsInCurrentLevel = np.append(wordsInCurrentLevel, words)
                    visited[link] = 1
                else:
                    if link in visited.keys():
                        visited[link] += 1
            allWords.append(list(wordsInCurrentLevel))
            allSentences.append(list(sentencesInCurrentLevel))
        else:
            URLsInCurrentLevel = []
            wordsInCurrentLevel = np.array([])
            sentencesInCurrentLevel = np.array([])
            for link in allURLs[-1]:
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    visited[link] = 1
                    try:
                        response = requests.get(link)
                        html_page = response.text
                        soup = BeautifulSoup(html_page, 'lxml')
                    except:
                        response.status_code = 404
                    links = []
                    if response.status_code != 404:
                        links = getLinksFromSoup(link, soup)
                        words, sentences = getWordsFromSoup(soup)
                        sentencesInCurrentLevel = np.append(
                            sentencesInCurrentLevel, sentences)
                        wordsInCurrentLevel = np.append(
                            wordsInCurrentLevel, words)
                        [URLsInCurrentLevel.append(
                            link) for link in links if link not in visited.keys()]
            allURLs.append(URLsInCurrentLevel)
            allWords.append(list(wordsInCurrentLevel))
            allSentences.append(list(sentencesInCurrentLevel))

    print(len(allURLs))
    wordCloudWords, countOfWordsPerLevel, averageLengthOfWordsPerLevel = analyzeWords(
        allWords)
    allBiagrams = getBigrams(allSentences)
    wordCloud = []
    bigramCloud = []
    for key, val in wordCloudWords:
        wordCloud.append({"x": key, "value": val, "category": key})
        # print(wordCloud)
    for key, val in allBiagrams:
        bigramCloud.append({"x": key, "value": val, "category": key})

    return (wordCloud, countOfWordsPerLevel,  averageLengthOfWordsPerLevel, bigramCloud)