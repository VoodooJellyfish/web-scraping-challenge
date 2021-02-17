#!/usr/bin/env python
# coding: utf-8

# In[1]:

def scrape():

# Dependencies
    from bs4 import BeautifulSoup
    import requests
    import os
    import pandas as pd
    import numpy as np
    import requests
    import pymongo
    import re
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


# In[3]:


#HTML to make calls from



# In[4]:


#Scraping for the first article headline
    results = soup.find_all('div', class_='content_title')

    header = []

    for result in results:
        news_title = result.find('a').text
        header.append(news_title)
    
    first_headline = header[0]


# In[5]:


#Scraping for the first body Paragraph
    teaser_results = soup.find_all('div', class_='rollover_description_inner')

    first_paragraph = []

    for result in teaser_results:
        news_teaser = result.text
        first_paragraph.append(news_teaser)

    first_paragraph = first_paragraph[0]


# In[6]:



    fact_url = "https://space-facts.com/mars/"


# In[7]:


#Using pandas to scan the fact_url for tabular data
    tables = pd.read_html(fact_url)



# In[8]:


    mars_df = tables[0]
    clean_df = mars_df.rename(columns= {0:"Attribute", 1:"Measurement"})



# In[9]:


    html_table = clean_df.to_html()



# In[10]:


    clean_df.to_html('mars_table.html')


# In[11]:


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



# In[12]:


    splinter_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(splinter_url)


# In[13]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    soup


# In[14]:


    hemi_links = soup.find_all('a', class_="itemLink")
    hemi_links


# In[15]:


    hemi_links = hemi_links[1::2]


# In[16]:


    link_list = []
    for hemi_link in hemi_links:
        h3 = hemi_link.find('h3').text
        link_list.append(h3)


# In[17]:



# In[18]:


    img_title_list = []
    img_link_list = []

    for link in link_list:
    
        browser.links.find_by_partial_text(link).click()
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        img_title = soup.find('h2', class_='title')
        img_title_list.append(img_title.text)
    
        links_with_text = []
    
        img_links = soup.find_all("a", href=re.compile("full.jpg")) 
    
        for a in img_links:
            if a.text: 
                links_with_text.append(a['href'])
    
        img_link_list.append(links_with_text)
    
    
        browser.back()
    browser.quit()


# In[22]:


#cleaning and making image dictionary list
    clean_list = []
    for link in img_link_list:
        cleaned = link[0]
        clean_list.append(cleaned)
    img_link_list = clean_list
    combined_list = list(zip(img_title_list,img_link_list))
    keys = ['title', 'img_url']
    img_dict = [{k:v for k,v in zip(keys, n)} for n in combined_list]
    print(img_dict)


# In[23]:





# In[24]:





# In[26]:





# In[27]:





# In[32]:


    dictionary = {"headline": first_headline,
              "summary": first_paragraph,
              'fact_table': html_table,
              'hemisphere_dicts': img_dict
            }

    return dictionary


# In[31]:





# In[ ]:




