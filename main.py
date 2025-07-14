#objective
#Building a sentiment analysis platform that tracks and visualizes public mood across Canadian provinces using Reddit, local news.
#• Engineered data pipeline to collect, clean, and process natural language content; stored structured data in MongoDB.
#• Applied NLP and unsupervised clustering to detect trends, keywords, and sentiment shifts; visualized results with a Plotly dashboard

import pandas as pd #data analysis
import numpy as np #md arrays
import sklearn as sk #algorithms
import nltk #natural language processing
import pymongo #MongoDB
import requests #HTTP requests
from bs4 import BeautifulSoup #web scraping
import plotly.express as px #visualization


#engineer a data pipeline

    #collect data - use beautifulsoup 
url = 'https://www.reddit.com/r/toronto/'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

print(soup) #can i just review the titles? i need to access the text content of posts

    #clean data

    #process natural language content - use VADER? or nltk

    #store data in MongoDB

    #do orchestration - apache kafka?

#apply NLP and unsupervised clustering

#visualize results with Plotly dashboard



