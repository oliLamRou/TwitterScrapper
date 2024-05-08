import os
import configparser

from _constant import CONFIG_PATH

class Config:
    CREDENTIAL = 'credential'
    HANDLE = 'handle'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)

    @property
    def username(self):
        return self.config[self.CREDENTIAL]['username']
    
    @property
    def password(self):
        return self.config[self.CREDENTIAL]['password']

    def create_config(self):
        #Credential section
        if not self.config.has_section(self.CREDENTIAL):
            self.config.add_section(self.CREDENTIAL)

        self.config[self.CREDENTIAL]['username'] = ''
        self.config[self.CREDENTIAL]['password'] = ''

        #Write on disk
        with open(CONFIG_PATH, 'w') as f:
            self.config.write(f)

    def check_config(self):
        #raise if no config file exist. Create a default file template for the user
        if not os.path.exists(CONFIG_PATH):
            self.create_config()
            raise ValueError(f'Config missing. Need to edit: {os.getcwd()}/{CONFIG_PATH}')

        #Check each param if it conform
        missing = 0
        if self.config[self.CREDENTIAL]['username'] == '':
            print('No username found')
            missing += 1

        if self.config[self.CREDENTIAL]['password'] == '':
            print('No password found')
            missing += 1

        if missing > 0:
            raise ValueError(f'Missing {missing} parameter. Edit: ./{CONFIG_PATH} before running again')

if __name__ == '__main__':
    Config().build()