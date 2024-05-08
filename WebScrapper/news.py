import os
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

class news:
	def __init__(self, search, limit):
		self.search = ''
		self.limit = 0
		self.df = DataFrame()
		self.driver = webdriver.Chrome()

	def stop(self):
		self.driver.quit()

	def set_df(self, path):
	    path = f'../data/raw/raw_gazette_{self.search}.csv'
	    if os.path.exists(path):
	        self.df = pd.read_csv(path)
	    else:
	        self.df = pd.DataFrame(columns=['raw_date', 'raw_title', 'raw_description', 'link'])

	def gazette(self):
		#Set DF with existing one or new one
		path = f'../data/raw/raw_gazette_{self.search}.csv'
		set_df(path)

	    results = 0
	    address = f'https://montrealgazette.com/search/?search_text={self.search}&date_range=-3650d&sort=desc&from={results}'
	    self.driver.get(address)
	    
	    while results < limit:
	        time.sleep(2)
	        for news in driver.find_elements(By.TAG_NAME, 'article'):
	            link = news.find_element(By.CLASS_NAME, 'article-card__link').get_attribute('href')
	            date = news.find_element(By.CLASS_NAME, 'article-card__time-clamp').text
	            title = news.find_element(By.CLASS_NAME, 'article-card__headline.text-size--extra-large--sm-up').text
	            description = news.find_element(By.TAG_NAME, 'p').text
	            self.df.loc[len(self.df.index)] = [date, title, description, link]
	                
	        results += 10
	        address = f'https://montrealgazette.com/search/?search_text={self.search}&date_range=-3650d&sort=desc&from={results}'
	        self.driver.get(address)

	        df.drop_duplicates().to_csv(path, index=False)
	        
	def j24h(search, limit):
	    path = f'../data/raw/raw_j24h_{search}.csv'
	    if os.path.exists(path):
	        df = pd.read_csv(path)
	    else:
	        df = pd.DataFrame(columns=['raw_date', 'raw_title', 'raw_description', 'link'])
	        
	    driver = webdriver.Chrome()
	    address = f'https://www.24heures.ca/recherche?q={search}&section='
	    driver.get(address)
	    
	    results = driver.find_element(By.CLASS_NAME, 'results-progress').text
	    
	    i = 0
	    while i < limit:
	        time.sleep(2)
	        page = driver.find_element(By.CLASS_NAME, 'results')
	        for news in page.find_elements(By.TAG_NAME, 'li'):
	            link = news.find_element(By.CLASS_NAME, 'clearfix').get_attribute('href')
	            date = news.find_element(By.CLASS_NAME, 'story-metas').text
	            title = news.find_element(By.CLASS_NAME, 'story-title').text
	            description = news.find_element(By.CLASS_NAME, 'story-excerpt').text
	            df.loc[len(df.index)] = [date, title, description, link]
	  
	        next_page = driver.find_element(By.CLASS_NAME, 'next')
	        next_page.click()
	        
	        time.sleep(1)
	        
	        if results == driver.find_element(By.CLASS_NAME, 'results-progress').text:
	            break
	            
	        results = driver.find_element(By.CLASS_NAME, 'results-progress').text
	        
	        i += 1
	        
	    df.drop_duplicates().to_csv(path, index=False)
	    driver.quit()

	def lapresse(search, start_page, end_page):
	    search_type = 'date' #or pertinence
	    path = f'../data/raw/raw_lapresse_{search}.csv'
	    if os.path.exists(path):
	        df = pd.read_csv(path)
	    else:
	        df = pd.DataFrame(columns=['raw_date', 'raw_title', 'raw_description', 'link'])
	        
	    driver = webdriver.Chrome()
	    
	    for i in range(start_page, end_page):
	        page = i
	        address = f'https://www.lapresse.ca/recherche?q={search}&p={page}&s={search_type}'
	        print(address)
	        driver.get(address)
	        time.sleep(2)

	        page = driver.find_element(By.CLASS_NAME, 'mostRecent.mostRecentList')

	        for news in page.find_elements(By.TAG_NAME, 'li'):
	            link = news.find_element(By.CLASS_NAME, 'visual').get_attribute('href')
	            date = news.find_element(By.TAG_NAME, 'time').text
	            title = news.find_element(By.CLASS_NAME, 'title.mostRecentCard__title').text
	            description = news.find_element(By.TAG_NAME, 'p').text
	            df.loc[len(df.index)] = [date, title, description, link]

	    driver.quit()
	    df.drop_duplicates().to_csv(path, index=False)