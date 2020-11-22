# Web Spider

This is **Jinesh Parakh's submission** for the **Avant Garde Engineering challenge Round 2**

## Problem Statement Chosen
Web spider – implement a “spider” that starts with one web page and follows to other websites mentioned on the previous web pages – up to pre-specified number of levels. The spider collects top N frequently used words on the linked sites and other statistics (your choice).

## Project's Overview


Description:


### 1. Tech Stack

a. **Python** for the core Spider Logic<br>
b. **NLTK  and Python** for analyzing the data<br>
c. **Flask** as the backend of the Web App<br>
d. **HTML, CSS, Bootstrap4, Javascript** for the Frontend of the App<br>
e. **Heroku** as a Cloud Platform for deployment of the Web App<br>


### 2. Instructions for Running the project Locally


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
