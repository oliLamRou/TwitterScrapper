import os
import sys
import time
import warnings
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

from _constant import CONFIG_PATH
from _config import Config

class Scrapper(Config):
    def __init__(self, config_path=None, silent=False):
        super().__init__()
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = CONFIG_PATH

        if silent:
            self.driver = self.set_driver
        else:
            self.driver = webdriver.Chrome()

        self.check_config()

        #Handle
        args = sys.argv
        if len(args) < 2 and len(args) > 3:
            print("Usage: python scrapper.py handle update(optionnal)")
            sys.exit(1)

        self.handle = args[1]
        if len(args) > 2 and args[2] == 'update':
            self.update = True

        self.address = f'https://twitter.com/{self.handle}'

        self.datadir = os.getcwd()
        self.filepath = f'{self.datadir}/scrap_twitter_{self.handle}.csv'

        self.df = pd.DataFrame()

    def stop(self):
        self.driver.quit()

    @property
    def set_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def login_twitter(self):
        print("Login Twitter...")
        sec = 5
        self.driver.get('https://x.com/i/flow/login')
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
        date = None

        if reset or os.path.exists(self.filepath) == False:
            self.df = pd.DataFrame(columns=['raw_date', 'raw_text'])
            self.address = f'https://x.com/search?q=(from%3A{self.handle})&src=typed_query&f=live'
            print(f'Scrapping from the latest post for Handle: {self.handle} in file: {self.filepath}')
        
        self.df = pd.read_csv(self.filepath).sort_values('raw_date')
        date = pd.to_datetime(self.df.raw_date, format='%Y-%m-%dT%H:%M:%S.000Z')
        if self.update:
            date = date.iloc[-1]
            date += timedelta(days=2)
            date = date.strftime('%Y-%m-%d')
            
            self.address = f'https://x.com/search?q=(from%3A{self.handle})%20since%3A{date}&src=typed_query&f=live'
            print(f'Ending {date} for Handle: {self.handle} in file: {self.filepath}')

        else:
            date = date.iloc[0]
            date += timedelta(days=2)
            date = date.strftime('%Y-%m-%d')
            
            self.address = f'https://x.com/search?q=(from%3A{self.handle})%20until%3A{date}&src=typed_query&f=live'
            print(f'Starting from {date} for Handle: {self.handle} in file: {self.filepath}')

    def scrap_twitter(self):
        self.driver.get(self.address)
        last_posts = []
        retry = 0

        post_id = set()
        time.sleep(2)
        while True:
            time.sleep(1)
            # self.driver.find_element(By.CLASS_NAME, 'css-175oi2r')
            posts = self.driver.find_elements(By.TAG_NAME, 'article')
            if posts == last_posts:
                if retry > 3:
                    break
                retry += 1
                print(f"Not finding more tweet. Trying {5-retry} more time")
            else:
                retry = 0

            last_posts = posts

            for post in posts:
                if post.id in post_id or post.text == 'This post is unavailable.':
                    continue

                post_id.add(post.id)
                raw_date = post.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                raw_text = []
                spans = post.find_elements(By.TAG_NAME, 'span')
                if not spans:
                    warnings.warn("Empty tweet...")

                for span in spans:
                    raw_text.append(span.text)
                    
                print('Adding: ', raw_date, ' '.join(raw_text)[:100])
                self.df.loc[len(self.df.index)] = [raw_date, raw_text]

            self.df.sort_values('raw_date', inplace=True)
            self.df.to_csv(self.filepath, index = False)
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)

        print('Nothing new or twitter kicked you out. Wait 30 min and start again.')

    def run(self):
        self.login_twitter()
        time.sleep(1)
        self.set_df()
        self.scrap_twitter()

if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()