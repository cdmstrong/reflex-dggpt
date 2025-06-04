
import os
from .weread_api import WeReadApi
from .notion_helper import NotionHelper
from .book import Book
from .weread import Weread
from .read_time import Read_time
class Weread_async():
    weread_api: WeReadApi
    notion_helper: NotionHelper
    book_api: Book
    weread: Weread
    read_time: Read_time

    def __init__(self, cookie, cc_id, cc_password, notion_token, page_id, vip_id):
        try:    

            self.weread_api = WeReadApi(cookie, cc_id, cc_password, vip_id)
            self.notion_helper = NotionHelper(token=notion_token, page_id=page_id, vip_id=vip_id)
            self.book_api = Book(self.weread_api, self.notion_helper, vip_id)
            self.weread = Weread(self.weread_api, self.notion_helper, vip_id)
            self.read_time = Read_time(self.weread_api, self.notion_helper, vip_id)
        except Exception as e:
            print(e)
            raise e

    def start_sync(self):
        # 同步书籍
        try:
            self.book_api.run()
            self.weread.run()
            # self.read_time.run()
        except Exception as e:
            print(e)
            raise e
        

# from dotenv import load_dotenv
# import os

# load_dotenv(override=True)
    
if __name__ == "__main__":
    # print(os.getenv("WERosD_COOKIE"))
    weread = Weread_async(os.getenv("WEREAD_COOKIE"), os.getenv("CC_ID"), os.getenv("CC_PASSWORD"), os.getenv("NOTION_TOKEN"), os.getenv("NOTION_PAGE"))
    weread.start_sync()