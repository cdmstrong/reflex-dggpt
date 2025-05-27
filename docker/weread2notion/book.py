import pendulum
from .notion_helper import NotionHelper
from .weread_api import WeReadApi
from .utils import *
from .config import book_properties_type_dict, tz


TAG_ICON_URL = "https://www.notion.so/icons/tag_gray.svg"
USER_ICON_URL = "https://www.notion.so/icons/user-circle-filled_gray.svg"
BOOK_ICON_URL = "https://www.notion.so/icons/book_gray.svg"
rating = {"poor": "⭐️", "fair": "⭐️⭐️⭐️", "good": "⭐️⭐️⭐️⭐️⭐️"}

class Book():
    def insert_book_to_notion(self, books, index, bookId):
        """插入Book到Notion"""
        book = {}
        if bookId in self.archive_dict:
            book["书架分类"] = self.archive_dict.get(bookId)
        if bookId in self.notion_books:
            book.update(self.notion_books.get(bookId))
        bookInfo = self.weread_api.get_bookinfo(bookId)
        if bookInfo != None:
            book.update(bookInfo)
        readInfo = self.weread_api.get_read_info(bookId)
        # 研究了下这个状态不知道什么情况有的虽然读了状态还是1 markedStatus = 1 想读 4 读完 其他为在读
        readInfo.update(readInfo.get("readDetail", {}))
        readInfo.update(readInfo.get("bookInfo", {}))
        book.update(readInfo)
        book["阅读进度"] = (
            100 if (book.get("markedStatus") == 4) else book.get("readingProgress", 0)
        ) / 100
        markedStatus = book.get("markedStatus")
        status = "想读"
        if markedStatus == 4:
            status = "已读"
        elif book.get("readingTime") and book.get("readingTime", 0) >= 60:
            status = "在读"
        book["阅读状态"] = status
        book["阅读时长"] = book.get("readingTime")
        book["阅读天数"] = book.get("totalReadDay")
        book["评分"] = book.get("newRating")
        if book.get("newRatingDetail") and book.get("newRatingDetail").get("myRating"):
            book["我的评分"] = rating.get(book.get("newRatingDetail").get("myRating"))
        elif status == "已读":
            book["我的评分"] = "未评分"
        book["时间"] = (
            book.get("finishedDate")
            or book.get("lastReadingDate")
            or book.get("readingBookDate")
        )
        book["开始阅读时间"] = book.get("beginReadingDate")
        book["最后阅读时间"] = book.get("lastReadingDate")
        cover = book.get("cover").replace("/s_", "/t7_")
        if not cover or not cover.strip() or not cover.startswith("http"):
            cover = BOOK_ICON_URL
        if bookId not in self.notion_books:
            book["书名"] = book.get("title")
            book["BookId"] = book.get("bookId")
            book["ISBN"] = book.get("isbn")
            book["链接"] = self.weread_api.get_url(bookId)
            book["简介"] = book.get("intro")
            book["作者"] = [
                self.notion_helper.get_relation_id(
                    x, self.notion_helper.author_database_id, USER_ICON_URL
                )
                for x in book.get("author").split(" ")
            ]
            if book.get("categories"):
                book["分类"] = [
                    self.notion_helper.get_relation_id(
                        x.get("title"), self.notion_helper.category_database_id, TAG_ICON_URL
                    )
                    for x in book.get("categories")
                ]
        properties = utils.get_properties(book, book_properties_type_dict)
        if book.get("时间"):
            self.notion_helper.get_date_relation(
                properties,
                pendulum.from_timestamp(book.get("时间"), tz="Asia/Shanghai"),
            )

        print(
            f"正在插入《{book.get('title')}》,一共{len(books)}本，当前是第{index+1}本。"
        )
        parent = {"database_id": self.notion_helper.book_database_id, "type": "database_id"}
        result = None
        if bookId in self.notion_books:
            result = self.notion_helper.update_page(
                page_id=self.notion_books.get(bookId).get("pageId"),
                properties=properties,
                cover=utils.get_icon(cover),
            )
        else:
            result = self.notion_helper.create_book_page(
                parent=parent,
                properties=properties,
                icon=utils.get_icon(cover),
            )
        page_id = result.get("id")
        if book.get("readDetail") and book.get("readDetail").get("data"):
            data = book.get("readDetail").get("data")
            data = {item.get("readDate"): item.get("readTime") for item in data}
            self.insert_read_data(page_id, data)


    def insert_read_data(self, page_id, readTimes):
        readTimes = dict(sorted(readTimes.items()))
        filter = {"property": "书架", "relation": {"contains": page_id}}
        results = self.notion_helper.query_all_by_book(self.notion_helper.read_database_id, filter)
        for result in results:
            timestamp = result.get("properties").get("时间戳").get("number")
            duration = result.get("properties").get("时长").get("number")
            id = result.get("id")
            if timestamp in readTimes:
                value = readTimes.pop(timestamp)
                if value != duration:
                    self.insert_to_notion(
                        page_id=id,
                        timestamp=timestamp,
                        duration=value,
                        book_database_id=page_id,
                    )
        for key, value in readTimes.items():
            self.insert_to_notion(None, int(key), value, page_id)


    def insert_to_notion(self, page_id, timestamp, duration, book_database_id):
        parent = {"database_id": self.notion_helper.read_database_id, "type": "database_id"}
        properties = {
            "标题": utils.get_title(
                pendulum.from_timestamp(timestamp, tz=tz).to_date_string()
            ),
            "日期": utils.get_date(
                start=pendulum.from_timestamp(timestamp, tz=tz).format(
                    "YYYY-MM-DD HH:mm:ss"
                )
            ),
            "时长": utils.get_number(duration),
            "时间戳": utils.get_number(timestamp),
            "书架": utils.get_relation([book_database_id]),
        }
        if page_id != None:
            self.notion_helper.client.pages.update(page_id=page_id, properties=properties)
        else:
            self.notion_helper.client.pages.create(
                parent=parent,
                icon=utils.get_icon("https://www.notion.so/icons/target_red.svg"),
                properties=properties,
            )


    def __init__(self, weread_api, notion_help):
        self.weread_api = weread_api
        self.notion_helper = notion_help
        self.archive_dict = {}
        self.notion_books = {}


    def run(self):
        try:
            bookshelf_books = self.weread_api.get_bookshelf()
            notion_books = self.notion_helper.get_all_book()
            bookProgress = bookshelf_books.get("bookProgress")
            bookProgress = {book.get("bookId"): book for book in bookProgress}
            for archive in bookshelf_books.get("archive"):
                name = archive.get("name")
                bookIds = archive.get("bookIds")
                self.archive_dict.update({bookId: name for bookId in bookIds})
            not_need_sync = []
            for key, value in notion_books.items():
                if (
                    (
                        key not in bookProgress
                        or value.get("readingTime") == bookProgress.get(key).get("readingTime")
                    )
                    and (self.archive_dict.get(key) == value.get("category"))
                    and (value.get("cover") is not None)
                    and (
                        value.get("status") != "已读"
                        or (value.get("status") == "已读" and value.get("myRating"))
                    )
                ):
                    not_need_sync.append(key)
            notebooks = self.weread_api.get_notebooklist()
            notebooks = [d["bookId"] for d in notebooks if "bookId" in d]
            books = bookshelf_books.get("books")
            books = [d["bookId"] for d in books if "bookId" in d]
            books = list((set(notebooks) | set(books)) - set(not_need_sync))
            for index, bookId in enumerate(books):
                self.insert_book_to_notion(books, index, bookId)
        except Exception as e:
            raise "get all books error"


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    weread_api = WeReadApi(os.getenv("WEREAD_COOKIE"), os.getenv("CC_ID"), os.getenv("CC_PASSWORD"))
    notion_helper = NotionHelper(os.getenv("NOTION_TOKEN"), os.getenv("NOTION_PAGE"))
    book = Book(weread_api, notion_helper)
    book.run()
