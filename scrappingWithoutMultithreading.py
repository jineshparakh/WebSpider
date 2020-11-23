'''
Importing all imports required for scrapping, crawling and analyzing the data from the webpages
'''
import requests
import cloudscraper
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

# Include the list of parents to blacklist, user can change it as per his will
blacklist = ['[document]', 'noscript', 'header',
             'html', 'meta','head', 'script', 'style']

'''
This function is used for getting all links from the Soup 
It is basically a nested function. The getLink(e) function takes a link and makes it a valid URL, if it is not already valid
The getLink function has all the possible types of URLs that could be gotten from the soup object. It makes them traversabale
'''
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
    '''
    It maps each link from the soup to the getLink function. After that the getLink function sends back valid URLs one by one
    '''        
    allLinks = list(map(getLink, soup.find_all('a', href=True))) 
    allLinks = [link for link in allLinks if link] #removing empty links from the links gotten from a page
    return list(set(allLinks)) #remove duplicates and return a list of links

'''
This function is used for getting all words from the soup
'''
def getWordsFromSoup(soup):
    text = soup.find_all(text=True) #finding out all the text from the soup
    output = ''
    outputSentences = []
    '''
    Cleaning the text received from the soup. Firstly we will remove all elements having their parents in blacklist 
    '''
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
            outputSentences.append('{} '.format(t))
    outputSentences = [i.strip() for i in outputSentences]
    # removing special characters
    outputSentences = [re.sub('[^a-zA-Z0-9]+', ' ', _)
                       for _ in outputSentences]
    # removing all only digit phrases       
    outputSentences = [' '.join(s for s in i.split() if not any(
        c.isdigit() for c in s)) for i in outputSentences]
    #removing empty sentences
    outputSentences = [i for i in outputSentences if i]
    #tokenising the sentence phrases using nltk
    outputSentences = [nltk.tokenize.sent_tokenize(i) for i in outputSentences]
    words = list(output.split(' '))
    words = [re.sub('[^a-zA-Z0-9]+', ' ', _) for _ in words]
    allWords = []
    #Filtering words and removing words having length less than 2 and numbers
    for word in words:
        if len(word) > 2:
            wordsInCurrent = word.split(' ')
            for w in wordsInCurrent:
                if len(w) > 2 and not(w.isdecimal()):
                    allWords.append(w.lower()) #appending lowercase words to the final list
    return allWords, outputSentences

'''
This function is used to get all bigrams(words coming together in pair) level by level from all the sentences and phrases we have gotten from the site
'''
def getBigrams(allSentences):
    allBiagrams = []
    for sentencesPerLevel in allSentences:
        bigram = []
        for sentence in sentencesPerLevel:
            token = nltk.word_tokenize(sentence) #tokenising the phrase
            token = [word.lower() for word in token if word not in stopwords.words('english')] #removing stopwords **only english
            bi = list(ngrams(token, 2)) #creating bigrams using ngrams
            [bigram.append(i[0]+" " + i[1]) for i in bi if i]
        [allBiagrams.append(i) for i in bigram]
    bigrams = {} #making a bigram frequency dictionary for plotting graphs
    for i in allBiagrams:
        bigrams[i] = bigrams.get(i, 0) + 1
    b = Counter(bigrams) 
    #return all the bigrams sorted in descending order of frequency
    return b.most_common()

'''
This function is used to analyze the words level by level for plotting graphs.
The statistics done are:
1. Count of Words Per Level including stopwords
2. Word Cloud with frequencies without stopwords
3. Average Length of Words Per Level including stopwords
'''
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
            word for word in wordsPerLevel if word not in stopwords.words('english')] #filtering words using nltk by removing stopwords in english only
        count = {}
        for i in filtered_words:
            count[i] = count.get(i, 0) + 1 #This dictionary can be used to analyze words individually per level
            words[i] = words.get(i, 0)+1
        c = Counter(count)
    w = Counter(words) #making a counter of the words
    return w.most_common(), countOfWordsPerLevel, averageLengthOfWordsPerLevel

'''
This is the main function for starting the scrapping. The parameters it takes are the baseURL and the maximum depth it has to go till.
I have used cloudscraper instead of requests so that it can handle cloudfare captchas upto some extent. However this opensource version does
not bypass all captchas
'''
def startScraping(baseURL, maxLevels):
    visited = {} # a visited dictionary to keep track of the visited links and also can be useful for counting how many times any URL occurs on a page
    allURLs = [] #a list to maintain the URLs per level
    allWords = [] #a list to maintain all the Words per level
    allSentences = [] # a list to maintain all the sentences and phrases per level
    
    for level in range(0, maxLevels+1):
        if level == 0:
            visited[baseURL] = 1 #marking the URL visited so that it will not be visited again
            scraper = cloudscraper.create_scraper() #creating a cloudscraper instance
            try:
                response=scraper.get(baseURL) #getting the page 
            except:
                continue    
            html_page = response.text #extracting text from the response
            soup = BeautifulSoup(html_page, 'lxml') #Creating a soup using the lxml parser

            if response.status_code != 404: #if the URL is found
                links = getLinksFromSoup(baseURL, soup) #calling the getLinks function to return all links on that webpage
                words, sentences = getWordsFromSoup(soup) #getting allWords and phrases/sentences from that webpage
                #modifing and inserting in respective lists
                allWords.append(words)
                s = []
                for sentence in sentences:
                    s.append(sentence[0])
                allSentences.append(list(s))
                allURLs.append(baseURL.split())
                allURLs.append(links)
        
        elif level == maxLevels:
            #if the level is maxLevel we will not find the links on these pages and just find the words and sentences.
            wordsInCurrentLevel = np.array([])
            sentencesInCurrentLevel = np.array([])
            for link in allURLs[-1]: #traversing all URL's received from the previous level
                #only visiting the unvisited URLs and not visiting mails, images, js, etc
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    scraper = cloudscraper.create_scraper() #create cloudscraper instance
                    try:
                        response=scraper.get(baseURL) #getting the page 
                    except:
                        continue  
                    html_page = response.text #extracting text from the response
                    soup = BeautifulSoup(html_page, 'lxml')
                    words, sentences = getWordsFromSoup(soup)
                    sentencesInCurrentLevel = np.append(
                        sentencesInCurrentLevel, sentences)
                    wordsInCurrentLevel = np.append(wordsInCurrentLevel, words)
                    visited[link] = 1 #marking the URL visited so that it will not be visited again
                else:
                    if link in visited.keys(): #if the link is already visited increase the counter to know about duplicate URLs
                        visited[link] += 1
            #adding to respective lists            
            allWords.append(list(wordsInCurrentLevel))
            allSentences.append(list(sentencesInCurrentLevel))
        
        else:
            URLsInCurrentLevel = []
            wordsInCurrentLevel = np.array([])
            sentencesInCurrentLevel = np.array([])
            for link in allURLs[-1]:
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    visited[link] = 1 #marking the URL visited so that it will not be visited again
                    try:
                        scraper = cloudscraper.create_scraper() #creating scrapper instance
                        try:
                            response=scraper.get(baseURL) #getting the page 
                        except:
                            continue  
                        html_page = response.text #extracting html page
                        soup = BeautifulSoup(html_page, 'lxml')
                    except:
                        response.status_code = 404
                    links = []
                    #similar process as the previous one, just this time as the level is not the ulimate one, also get the Links on each page
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
    
    #analyzing the data gotten from crawling
    wordCloudWords, countOfWordsPerLevel, averageLengthOfWordsPerLevel = analyzeWords(
        allWords)
    #getting bigrams from sentences and phrases    
    allBiagrams = getBigrams(allSentences)
    wordCloud = []
    bigramCloud = []
    #formatting the wordCloudWords and allBiagrams for the plotting of graphs
    for key, val in wordCloudWords:
        wordCloud.append({"x": key, "value": val, "category": key})
    for key, val in allBiagrams:
        bigramCloud.append({"x": key, "value": val, "category": key})

    return (wordCloud, countOfWordsPerLevel,  averageLengthOfWordsPerLevel, bigramCloud)



# BASE_URL='https://www.ubs.com/in/en.html'
# MAX_LEVEL=2


# wordCloud, wordsInEachLevel, AvarageLengthOfWordsInEachLevel, bigramCloud = startScraping(BASE_URL, MAX_LEVEL-1)    