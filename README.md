# Web Spider

This is **Jinesh Parakh's submission** for the **UBS Avant Garde Engineering Challenge Round 2**

## Problem Statement Chosen
Web spider – implement a “spider” that starts with one web page and follows to other websites mentioned on the previous web pages – up to pre-specified number of levels. The spider collects top N frequently used words on the linked sites and other statistics (your choice).

## Project's Overview


### 1. Description

**Web Spider<sup>(&beta;)</sup>** is an **N level Web Crawler** which *dives N levels deep and extracts data from the webpages to provide valuable insights and statistics on the data scrapped.* It used a ***Breadth First Search*** type of approach for crawling the web. It **crawls through webpages level by level and extracts words and sentences/phrases from them to give some wonderful statistical insights on the data extracted**. 

You can find the deployed project [here](https://my-web-spider.herokuapp.com/)

### 2. Statistics and features

a. **NLP based Color Range inclusive Word Cloud** with *frequencies and percentage occurrence of words on the crawled sites*<br>
b. **NLP based Color Range inclusive Bigram Cloud** with *frequencies and percentage occurrence of words on the crawled sites*<br>
c. **Bar Graph** denoting the *Words in Each Level of Search*<br>
d. **Line Chart** denoting the *Average Length of words in Each Level of Search*<br>
e. **Search Bar** for *queries to check whether the word exists in the crawled sites or not and even find the frequency of occurance*<br>
f. **Responsive and User Friendly** *User Interface* for the best User Experience<br>



### 3. Tech Stack

a. **Python** for the core Spider Logic<br>
b. **NLTK  and Python** for analyzing the data<br>
c. **Flask** as the backend of the Web App<br>
d. **HTML, CSS, Bootstrap4, Javascript** for the Frontend of the App and to display the statistics<br>
e. **Heroku** as a Cloud Platform for deployment of the Web App<br>


### 4. Instructions for Running and Testing the project Locally


**a. Clone the repository (Otherwise you can also download the zip file of the repository)**
```
> git clone https://git-rba.hackerrank.com/git/42fc048c-aca2-4ace-874f-9a26af71349f
```

**b. Change the directory. (You can also open this project on any IDE, preferably VSCode)**

```
> cd 42fc048c-aca2-4ace-874f-9a26af71349f
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
*On MacOS and Linux (Tested on MacOs Catlina)*
```
> source venv/bin/activate   #Activate Virtual Environment
```

**d. Installing requirements**
```
> pip install -r requirements.txt    #Installing all the requirements for running the project
```

**e. Once all the requirements are installed, it's time to run the Flask App**
```
> python app.py    #Starts the Server
```

Once the server starts, go to http://127.0.0.1:5000/ to enjoy analyses based on Crawling the URLs

**f. Testing the App with Unit Test Cases**
```
> nose2 testcases    #Running Unit Test Cases for the Flask App
```

### 6. Assumptions

1. The sites for which the crawling will be done will contain English words only. This is because while filtering stopwords, only English language stopwords are filtered<br>
2. Currently, in the web App the depth to crawl upto is limited to 2 levels only. This is due to the time constraint for extraction of data. <br>
3. The 

### 7. Current Shortcomings

1. The deployed App has a timeout of 30s for getting the response. But that much time is not sufficient for crawling some websites with levels 2 or more.<br>
2. Cloudflare version 2 Captcha challenge cannot be passed by the deployed App. The opensource version of **cloudscraper** does not provide this feature.
Example where the challenge occurs: https://pict.edu/ <br>
3. Due to huge amount of data the crawler takes extra time to crawl for levels 2 and above<br>
4. The spider finds it difficult to get the most recent DOM elements that is generated by Javascript async calls (AJAX, etc) due to use of Beautiful Soup.<br>


### 8. References

a. https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319
