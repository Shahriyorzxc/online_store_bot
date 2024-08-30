import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.getBotEnv()
        self.db_laptop()

    def getBotEnv(self):
        self.token = os.getenv("TOKEN", "defaultbottoken")
        self.click_token = os.getenv("CLICK_TOKEN", "defaultclicktoken")

    def db_laptop(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "postgres")
        self.db = os.getenv("DB_NAME", "laptop_db")
        self.password = os.getenv("DB_PASSWORD", "123456")
