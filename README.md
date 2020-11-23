# Web Spider

Welcome to **[Jinesh Parakh's](https://github.com/jineshparakh) submission** for the **UBS Avant Garde Engineering Challenge Round 2(UBS Project X Code Challenge Round II)**

## Problem Statement Chosen
Web spider – implement a “spider” that starts with one web page and follows to other websites mentioned on the previous web pages – up to pre-specified number of levels. The spider collects top N frequently used words on the linked sites and other statistics (your choice).

## Project's Overview


### 1. Description

**Web Spider<sup>(&beta;)</sup>** is an **N level Multithreaded Web Spider** which *dives N levels deep and extracts data from the webpages to provide valuable insights and statistics on the data scrapped.* It used a ***Breadth First Search*** type of approach for crawling the web. It **crawls through webpages level by level in an asynchronous manner using multithreading and extracts words and sentences/phrases from them to give some wonderful statistical insights on the data extracted**. 

You can find the deployed project [here](https://my-web-spider.herokuapp.com/)

### 2. Statistics and features

a. **NLP based Color Range inclusive Word Cloud** with *frequencies and percentage occurrence of words on the crawled sites*<br>
b. **NLP based Color Range inclusive Bigram Cloud** with *frequencies and percentage occurrence of words on the crawled sites*<br>
c. **Bar Graph** denoting the *Words in Each Level of Search*<br>
d. **Line Chart** denoting the *Average Length of words in Each Level of Search*<br>
e. **Search Bar** for *queries to check whether the word exists in the crawled sites or not and even find the frequency of occurrence*<br>
f. **Responsive and User-Friendly** *User Interface* for the Best User Experience<br>



### 3. Tech Stack

a. **Python** for the core Spider Logic<br>
b. **NLTK  and Python** for cleaning and analyzing the data<br>
c. **Flask** as the backend of the Web App<br>
d. **HTML, CSS, Bootstrap4, Javascript** for the Frontend of the App and to display the statistics<br>
e. **Heroku** as a Cloud Platform for the deployment of the Web App<br>


### 4. Instructions for Running and Testing the project Locally


**a. Clone the repository (Otherwise you can also download the zip file of the repository)**
```
> git clone https://github.com/jineshparakh/WebCrawler.git
```

**b. Change the directory. (You can also open this project on any IDE, preferably VSCode)**

```
> cd WebCrawler
```

**c. Setting Up Virtual Environment(Prerequisites: Your System should have Python3 installed)**

```
> pip install virtualenv    #Installing the virtual environment module
> virtualenv venv           #Create virtual environment venv
````
**d. Activating Virtual Environment:**<br><br>
*On Windows (Tested on Windows 10)*
```
> venv\Scripts\activate    #Activate Virtual Environment 
```
*On macOS  and Linux (Tested on MacOs Catlina)*
```
> source venv/bin/activate   #Activate Virtual Environment
```

**e. Installing requirements**
```
> pip install -r requirements.txt    #Installing all the requirements for running the project
```

**f. Once all the requirements are installed, it's time to run the Flask App**
```
> python app.py    #Starts the Server
```

Once the server starts, go to http://127.0.0.1:5000/ to enjoy analyses based on Crawling the URLs

**g. Testing the App with Unit Test Cases**
```
> nose2 testcases    #Running Unit Test Cases for the Flask App
```
### 5. Screenshots

#### The Default Landing Page
![The Default Landing Page](/Screenshots/Demo1.png)
<br><br><br>
#### The Waiting Screen After the Crawling Starts
![The Waiting Screen After the Crawling Startse](/Screenshots/Demo2.png)
<br><br><br>
#### The Word Cloud
![The Word Cloud](/Screenshots/Demo3.png)
<br><br><br>
#### The Bigram Cloud
![The Bigram Cloud](/Screenshots/Demo4.png)
<br><br><br>
#### Bar Graph denoting Count of Words Per Level
![Bar Graph denoting Count of Words Per Level](/Screenshots/Demo5.png)
<br><br><br>
#### Line Chart denoting the average length of words per level
![Line Chart denoting the average length of words per level](/Screenshots/Demo6.png)
<br><br><br>
#### The search Query Feature
![The search Query Feature](/Screenshots/Demo7.png)
<br><br><br>



### 6. Performance with and without Multithreading

![Performance With and Without Mulithreading](/Screenshots/TimeDifference.png)

**The base URL taken:** https://www.ubs.com/in/en.html<br>
**Depth:** 2<br>

The first Measure-Command calculates the time taken for the spider to crawl data using **Multithreading and async calls**<br>
The second Measure-Command calculates the time taken for the spider to crawl the data **without the use of Multithreading**<br>

*Time taken in the first case ≈ 63.42s*<br>
*Time taken in the second case ≈ 190.90s*

Approximate percentage increase reducing time complexity using Multithreading and async calls ≈ **201.009% increase**<br>

### 6. Assumptions

1. The sites for which the crawling will be done will contain English words only. This is because while filtering stopwords, only English language stopwords are filtered.<br>
2. Currently, in the web App, the depth to crawl up to is limited to 2 levels only. This is due to the Request timeout constraint for extraction of data set by Heroku. <br>


### 7. Current Shortcomings

1. The deployed App has a timeout of 30s for getting the response (set by Heroku). But that much time is not sufficient for crawling some websites with levels 2 or more.<br>
2. The spider finds it difficult to get the most recent DOM elements that are generated by Javascript async calls (AJAX, etc) due to the use of Beautiful Soup.<br>
3. The spider finds it difficult to bypass Captcha.<br>


### 8. Major References

a. https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319<br>
b. https://www.patricksoftwareblog.com/unit-testing-a-flask-application/<br>
c. https://towardsdatascience.com/website-data-cleaning-in-python-for-nlp-dda282a7a871<br>
d. https://docs.anychart.com/Quick_Start/Quick_Start<br>
e. https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python<br>
g. https://getbootstrap.com/docs/4.0/<br>
h. https://flask.palletsprojects.com/en/1.1.x/<br>
i. https://stackoverflow.com/<br>
j. https://docs.python.org/3/<br>
k. https://www.youtube.com/watch?v=L2CxFhkZrss<br>
