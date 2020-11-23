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
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Include the list of parents to blacklist, user can change it as per his will
blacklist = ['[document]', 'noscript', 'header',
             'html', 'meta','head', 'script', 'style']

'''
This function is used for getting all links from the Soup 
It is basically a nested function. The getLink(e) function takes a link and makes it a valid URL, if it is not already valid
The getLink function has all the possible types of URLs that could be gotten from the soup object. It makes them traversabale
'''
def getLinksFromLinkAndSession(baseURL, session): 
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
    try:   
        response=session.get(baseURL) #getting the page
    except:
        return []     
    if response.ok:
        html_page = response.text #extracting text from the response
        soup = BeautifulSoup(html_page, 'lxml') #Creating a soup using the lxml parser
        allLinks = list(map(getLink, soup.find_all('a', href=True))) 
        allLinks = [link for link in allLinks if link] #removing empty links from the links gotten from a page
        return list(set(allLinks)) #remove duplicates and return a list of links
    else:    
        return []    

'''
This function is used for getting all words from the soup
'''
def getWordsAndSentencesFromLinkAndSession(link, session):
    try:
        response=session.get(link) #getting the page
    except:
        return [],[]     
    if response.ok:
        html_page = response.text #extracting text from the response
        soup = BeautifulSoup(html_page, 'lxml') #Creating a soup using the lxml parser
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
    else:    
        return [],[]    

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
        averageLengthOfWordsPerLevel.append(["Level "+str(level), sum(len(s) for s in wordsPerLevel)/len(wordsPerLevel)])
        level += 1
        filtered_words = [word for word in wordsPerLevel if word not in stopwords.words('english')] #filtering words using nltk by removing stopwords in english only
        count = {}

        for i in filtered_words:
            count[i] = count.get(i, 0) + 1 #This dictionary can be used to analyze words individually per level
            words[i] = words.get(i, 0)+1
        c = Counter(count)

    w = Counter(words) #making a counter of the words

    return w.most_common(), countOfWordsPerLevel, averageLengthOfWordsPerLevel

'''
The next two functions use multithreading for asynchronous crawling and gathering of data reveived by extraction of data from a list of URLs.
These functions ensure that the crawling is done asynchronously and hence speeds up the process.
'''
async def threadPoolForGettingWordsAndLinks(URLs):
    #using numpy arrays for faster append operation
    wordsInCurrentLevel=np.array([])
    sentenceInCurrentLevel=np.array([])
    linksInNextLevel=np.array([])
    with ThreadPoolExecutor(max_workers=len(URLs)) as executor:
        with requests.Session() as session:
            loop=asyncio.get_event_loop()
            #the tasks to perform, here two tasks are performed in concurrency
            tasks=[
                [loop.run_in_executor(executor, getWordsAndSentencesFromLinkAndSession, *(link, session)) for link in URLs],
                [loop.run_in_executor(executor, getLinksFromLinkAndSession, *(link, session)) for link in URLs]
            ]
        #appending data gathered from crawling to the numpy arrays            
        for words, sentences in await asyncio.gather(*tasks[0]):
            wordsInCurrentLevel=np.append(wordsInCurrentLevel, words)
            sentenceInCurrentLevel=np.append(sentenceInCurrentLevel,sentences) 
        for links in await asyncio.gather(*tasks[1]):
            linksInNextLevel=np.append(linksInNextLevel,links)    

    return list(wordsInCurrentLevel),list(sentenceInCurrentLevel), list(linksInNextLevel)


async def threadPoolForGettingWords(URLs):
    #using numpy arrays for faster append operation
    wordsInCurrentLevel=np.array([])
    sentenceInCurrentLevel=np.array([])
    #the threadPoolExecutor Service
    with ThreadPoolExecutor(max_workers=max(1,len(URLs))) as executor:
        with requests.Session() as session:
            loop=asyncio.get_event_loop()
            #the tasks to perform
            tasks=[
                [loop.run_in_executor(executor, getWordsAndSentencesFromLinkAndSession, *(link, session)) for link in URLs]
                ]
        #appending data gathered from crawling to the numpy arrays        
        for words, sentences in await asyncio.gather(*tasks[0]):
            wordsInCurrentLevel=np.append(wordsInCurrentLevel, words)
            sentenceInCurrentLevel=np.append(sentenceInCurrentLevel,sentences)  

    return list(wordsInCurrentLevel),list(sentenceInCurrentLevel)   

'''
This is the main function for starting the scrapping and crawling. The parameters it takes are the baseURL and the maximum depth it has to go till.
Multithreading using asyncio and ThreadPoolExecutor for faster gathering of information during crawling.
'''
def startScraping(baseURL, maxLevels):
    visited = {} # a visited dictionary to keep track of the visited links and also can be useful for counting how many times any URL occurs on a page
    allURLs = [] #a list to maintain the URLs per level
    allWords = [] #a list to maintain all the Words per level
    allSentences = [] # a list to maintain all the sentences and phrases per level
    
    for level in range(0, maxLevels+1):
        if level == 0:
            visited[baseURL] = 1 #marking the URL visited so that it will not be visited again
            l=[]
            l.append(baseURL)
            loop = asyncio.new_event_loop() #starting a new event loop
            asyncio.set_event_loop(loop) #setting the loop
            allURLs.append(l)
            '''
            If the current level(0) is the maxLevel then we don't need to search for URLs on that page.
            Else we need to search for URLs on that page
            '''
            if level==maxLevels:
                future=asyncio.ensure_future(threadPoolForGettingWords(l))
                #running the process until all the data is gathered
                wordsInCurrentLevel,sentences=loop.run_until_complete(future) 

                #adding to respective lists
                allWords.append(wordsInCurrentLevel)
                allSentences.append(sentences)
            else:
                future=asyncio.ensure_future(threadPoolForGettingWordsAndLinks(l))
                #running the process until all the data is gathered
                wordsInCurrentLevel,sentencesInCurrentLevel, LinksInNextLevel=loop.run_until_complete(future)

                #adding to respective lists
                allWords.append(wordsInCurrentLevel)
                allSentences.append(sentencesInCurrentLevel)
                allURLs.append(LinksInNextLevel)
        
        elif level == maxLevels:
            #if the level is maxLevel we will not find the links on these pages and just find the words and sentences.
            URLs=[] #list to hold valid URLs in current level
            for link in allURLs[-1]:
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    URLs.append(link)
                    visited[link]=1
                else:
                    if link in visited.keys(): #if the link is already visited increase the counter to know about duplicate URLs
                        visited[link] += 1

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            future=asyncio.ensure_future(threadPoolForGettingWords(URLs)) #running the process until all the data is gathered
            wordsInCurrentLevel,sentencesInCurrentLevel=loop.run_until_complete(future)    
            
            #adding to respective lists           
            allWords.append(wordsInCurrentLevel)
            allSentences.append(sentencesInCurrentLevel)
        else:
            URLs = [] #list to hold valid URLs in current level
            for link in allURLs[-1]:
                if link not in visited.keys() and ((not link.startswith("mailto:")) and (not ("javascript:" in link)) and (not link.endswith(".png")) and (not link.endswith(".jpg")) and (not link.endswith(".jpeg"))):
                    visited[link] = 1 #marking the URL visited so that it will not be visited again
                    URLs.append(link)
                else:
                    if link in visited.keys():
                        visited[link]+=1

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)            
            future=asyncio.ensure_future(threadPoolForGettingWordsAndLinks(URLs))
            wordsInCurrentLevel,sentencesInCurrentLevel, URLsInNextLevel=loop.run_until_complete(future)      

            #adding to respective lists
            allURLs.append(URLsInNextLevel)
            allWords.append(wordsInCurrentLevel)
            allSentences.append(sentencesInCurrentLevel)
    

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

