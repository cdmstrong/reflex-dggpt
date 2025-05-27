
from .weread_api import WeReadApi
from .notion_helper import NotionHelper
from .book import Book
from .weread import Weread
from .read_time import Read_time
class Weread_async():
    # _instance = None
    # is_init = False

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(Weread_async, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self, cookie,  cc_id, cc_password, notion_token, page_id):
    #     if self.is_init:
    #         return
        self.weread_api = WeReadApi(cookie, cc_id, cc_password)
        self.notion_helper = NotionHelper(notion_token, page_id)
        self.book_api = Book(self.weread_api, self.notion_helper)
        self.weread = Weread(self.weread_api, self.notion_helper)
        self.read_time = Read_time(self.weread_api, self.notion_helper)

    def start_sync(self):
        # 同步书籍
        self.book_api.run()
        self.weread.run()
        # self.read_time.run()
        

from dotenv import load_dotenv
import os

load_dotenv(override=True)
    
if __name__ == "__main__":
    # print(os.getenv("WEREAD_COOKIE"))
    weread = Weread_async(os.getenv("WEREAD_COOKIE"), os.getenv("CC_ID"), os.getenv("CC_PASSWORD"), os.getenv("NOTION_TOKEN"), os.getenv("NOTION_PAGE"))
    weread.start_sync()