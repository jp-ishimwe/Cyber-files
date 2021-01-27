# Web scraping, pickle imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import numpy as np
import ssl

root_url = 'https://igihe.com/'

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

def get_url(main_url, root_url, number_of_articles=1):
    
    page = requests.get(main_url).content
    soup = BeautifulSoup(page, "html5lib")
    new_papers = soup.find_all("span", class_="homenews-title")
    tags = soup.find_all("div", class_="col col-lg-3 col-md-3 col-sm-3 col-xs-3")
    news_li = soup.find_all("ul")

    
    links = []
    tags_set = set()
    
    for n in range(0, number_of_articles):
        try:
            link = new_papers[n].find('a')['href']
            links.append(root_url+link)
            
            link1 = tags[n].find('a')['href']
            if link1 is not None:
                tags_set.add(root_url+link1)
            
        except IndexError:
            pass

    tags_set = list(tags_set)
    return links, tags_set

# Get all the links
main_urls = [] # define all sub urls like: 'https://igihe.com/imikino/',
All_urls = []
number_of_articles = 21
tags = []

for main_url in main_urls:
    try:        
        links, tags_set = get_url(main_url, root_url, number_of_articles)
        tags.extend(tags_set)
        All_urls.extend(links)
        
    except TypeError:
        pass
tags = list(set(tags))  
All_urls = list(set(All_urls))

# get the text from the webpage

def url_to_text(url):
    page = requests.get(url, verify=ssl.CERT_NONE, headers=headers).text
    soup = BeautifulSoup(page, "lxml")
    title = soup.find('h3', class_="title-article").text if soup.find('h3', class_="title-article") else ''
    body_class = soup.find(class_="fulltext margintop10")
    text = []
    unused_links = []
    if body_class:
        text = [p.text for p in body_class.find_all('p')]
    else:
        unused_links.append(url)        
    return text, unused_links, title

new_papers = All_urls + tages
text_titles = [url_to_text(u) for u in new_papers]
text = [txt[0] for txt in text_titles]
titles = [title[0] for title in text_titles]

data = {'article-title': titles, 'text': text}
df = pd.DataFrame(data)

def clean_data(data):
    x = data.strip()
    x = re.sub(r"\['",'',x)
    x = re.sub(r"'\]",'',x)
    x = re.sub(r'[,?!-]+', '.', x)
    x = re.sub(r'http\S+','', x)
    x = re.findall(r'\w+', x)
    x = ' '.join(x)
    return x

df['clean_text'] = df.text.apply(clean_data)
df.to_csv('kinyarwanda_news_dump.csv', index=False)

