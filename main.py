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

import requests
from bs4 import BeautifulSoup

#engineer a data pipeline

    #collect data - use beautifulsoup 
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_reddit_data(subreddit):
    #old.reddit.com has simple html structure
    url = f'https://old.reddit.com/r/{subreddit}/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    posts = []
    
    #scrape posts
    for post in soup.find_all('div', class_='thing'):
        title = post.find('a', class_='title').text
        post_url = post.find('a', class_='title')['href']
        
        #go into post and find content + comments
        if post_url.startswith('/r/'):
            post_url = f'https://old.reddit.com{post_url}'
            
        post_data = get_post_content(post_url)
        
        posts.append({
            'title': title,
            'url': post_url,
            'content': post_data['content'],
            'comments': post_data['comments']
        })
    
    return posts

def get_post_content(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #post content
    content = ''
    content_div = soup.find('div', class_='usertext-body')
    if content_div:
        content = content_div.text.strip()
    
    #comments
    comments = []
    comment_area = soup.find('div', class_='commentarea')
    if comment_area:
        for comment in comment_area.find_all('div', class_='usertext-body'):
            comments.append(comment.text.strip())
    
    return {
        'content': content,
        'comments': comments
    }

#example for now
subreddit = 'toronto'
posts = get_reddit_data(subreddit)

import json
with open(f'{subreddit}_data.json', 'w') as f:
    json.dump(posts, f, ensure_ascii=False, indent=4) #

    #process natural language content - use VADER? or nltk

    #store data in MongoDB

    #do orchestration - apache kafka?

#apply NLP and unsupervised clustering

#visualize results with Plotly dashboard



