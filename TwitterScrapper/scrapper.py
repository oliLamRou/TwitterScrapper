import os
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

class Twitter:
    def __init__(self, handle, silent=True):
        self.password = ''
        self.username = ''
        self.credential()

        if silent:
            self.driver = self.set_driver
        else:
            self.driver = webdriver.Chrome()

        self.handle = handle
        self.address = f'https://twitter.com/{self.handle}'

        self.df = pd.DataFrame()

    def stop(self):
        self.driver.quit()

    def credential(self):
        "Return username and password from .config"
        with open('./credential.config', 'r') as f:
            credential = f.read().split()
            self.username = credential[0]
            self.password = credential[1]

    @property
    def set_driver(self):
        options = webdriver.ChromeOptions() 
        options.add_argument("--headless") 
        return webdriver.Chrome(options=options)

    def login_twitter(self):
        sec = 3
        self.driver.get('https://twitter.com/i/flow/login')
        time.sleep(sec)

        username_field = self.driver.find_element(By.TAG_NAME, 'input')
        time.sleep(sec)
        username_field.send_keys(self.username)
        time.sleep(sec)
        username_field.send_keys(Keys.RETURN)
        time.sleep(sec)

        password_field = self.driver.find_elements(By.TAG_NAME, 'input')
        password_field[1].send_keys(self.password)
        time.sleep(sec)
        password_field[1].send_keys(Keys.RETURN)
        time.sleep(sec)

    def set_df(self, reset=False):
        path = f'../data/raw/raw_twitter_{handle}.csv'        
        date = None

        if reset or os.path.exists(path) == False:
            df = pd.DataFrame(columns=['raw_date', 'raw_text'])
            self.address = f'https://twitter.com/{handle}'
        else:
            df = pd.read_csv(path)
            date = pd.to_datetime(df.raw_date, format='%Y-%m-%dT%H:%M:%S.000Z').sort_values(ascending=False).iloc[-1]
            date += timedelta(days=2)
            date = date.strftime('%Y-%m-%d')
            
            self.address = f'https://twitter.com/search?q=(from%3A{handle})%20until%3A{date}&src=typed_query&f=live'
            print(self.address)

    def scrap_twitter(self):
        self.driver.get(self.address)

        post_id = set()
        time.sleep(2)
        while True:
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'css-175oi2r')
            posts = driver.find_elements(By.TAG_NAME, 'article')
            for post in posts:
                if post.id in post_id or post.text == 'This post is unavailable.':
                    continue

                post_id.add(post.id)
                raw_date = post.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                raw_text = []
                for span in post.find_elements(By.CLASS_NAME, 'css-1qaijid.r-bcqeeo.r-qvutc0.r-poiln3'):
                    raw_text.append(span.text)
                    
                print('Adding: ', raw_date)
                df.loc[len(df.index)] = [raw_date, raw_text]

            df.to_csv(f'../data/raw/raw_twitter_{handle}.csv', index = False)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)

    def run(self):
        self.login_twitter()
        self.set_df()
        #NOTE: This won't run
        self.scrap_twitter()


if __name__ == '__main__':
    pass

