from utils.logs import VipLogManager
from .notion_helper import NotionHelper
from .weread_api import WeReadApi

from .utils import (
    get_block,
    get_heading,
    get_number,
    get_number_from_result,
    get_quote,
    get_rich_text_from_result,
    get_table_of_contents,
)

class Weread():

    def get_bookmark_list(self, page_id, bookId):
        """获取我的划线"""
        filter = {
            "and": [
                {"property": "书籍", "relation": {"contains": page_id}},
                {"property": "blockId", "rich_text": {"is_not_empty": True}},
            ]
        }
        results = self.notion_helper.query_all_by_book(
            self.notion_helper.bookmark_database_id, filter
        )
        dict1 = {
            get_rich_text_from_result(x, "bookmarkId"): get_rich_text_from_result(
                x, "blockId"
            )
            for x in results
        }
        dict2 = {get_rich_text_from_result(x, "blockId"): x.get("id") for x in results}
        bookmarks = self.weread_api.get_bookmark_list(bookId)
        for i in bookmarks:
            if i.get("bookmarkId") in dict1:
                i["blockId"] = dict1.pop(i.get("bookmarkId"))
        for blockId in dict1.values():
            self.notion_helper.delete_block(blockId)
            self.notion_helper.delete_block(dict2.get(blockId))
        return bookmarks


    def get_review_list(self, page_id,bookId):
        """获取笔记"""
        filter = {
            "and": [
                {"property": "书籍", "relation": {"contains": page_id}},
                {"property": "blockId", "rich_text": {"is_not_empty": True}},
            ]
        }
        results = self.notion_helper.query_all_by_book(self.notion_helper.review_database_id, filter)
        dict1 = {
            get_rich_text_from_result(x, "reviewId"): get_rich_text_from_result(
                x, "blockId"
            )
            for x in results
        }
        dict2 = {get_rich_text_from_result(x, "blockId"): x.get("id") for x in results}
        reviews = self.weread_api.get_review_list(bookId)
        for i in reviews:
            if i.get("reviewId") in dict1:
                i["blockId"] = dict1.pop(i.get("reviewId"))
        for blockId in dict1.values():
            self.notion_helper.delete_block(blockId)
            self.notion_helper.delete_block(dict2.get(blockId))
        return reviews


    def check(self, bookId):
        """检查是否已经插入过"""
        filter = {"property": "BookId", "rich_text": {"equals": bookId}}
        response = self.notion_helper.query(
            database_id=self.notion_helper.book_database_id, filter=filter
        )
        if len(response["results"]) > 0:
            return response["results"][0]["id"]
        return None


    def get_sort(self):
        """获取database中的最新时间"""
        filter = {"property": "Sort", "number": {"is_not_empty": True}}
        sorts = [
            {
                "property": "Sort",
                "direction": "descending",
            }
        ]
        response = self.notion_helper.query(
            database_id=self.notion_helper.book_database_id,
            filter=filter,
            sorts=sorts,
            page_size=1,
        )
        if len(response.get("results")) == 1:
            return response.get("results")[0].get("properties").get("Sort").get("number")
        return 0



    def sort_notes(self, page_id, chapter, bookmark_list):
        """对笔记进行排序"""
        bookmark_list = sorted(
            bookmark_list,
            key=lambda x: (
                x.get("chapterUid", 1),
                0
                if (x.get("range", "") == "" or x.get("range").split("-")[0] == "")
                else int(x.get("range").split("-")[0]),
            ),
        )

        notes = []
        if chapter != None:
            filter = {"property": "书籍", "relation": {"contains": page_id}}
            results = self.notion_helper.query_all_by_book(
                self.notion_helper.chapter_database_id, filter
            )
            dict1 = {
                get_number_from_result(x, "chapterUid"): get_rich_text_from_result(
                    x, "blockId"
                )
                for x in results
            }
            dict2 = {get_rich_text_from_result(x, "blockId"): x.get("id") for x in results}
            d = {}
            for data in bookmark_list:
                chapterUid = data.get("chapterUid", 1)
                if chapterUid not in d:
                    d[chapterUid] = []
                d[chapterUid].append(data)
            for key, value in d.items():
                if key in chapter:
                    if key in dict1:
                        chapter.get(key)["blockId"] = dict1.pop(key)
                    notes.append(chapter.get(key))
                notes.extend(value)
            for blockId in dict1.values():
                self.notion_helper.delete_block(blockId)
                self.notion_helper.delete_block(dict2.get(blockId))
        else:
            notes.extend(bookmark_list)
        return notes


    def append_blocks(self, id, contents):
        print(f"笔记数{len(contents)}")
        before_block_id = ""
        block_children = self.notion_helper.get_block_children(id)
        if len(block_children) > 0 and block_children[0].get("type") == "table_of_contents":
            before_block_id = block_children[0].get("id")
        else:
            response = self.notion_helper.append_blocks(
                block_id=id, children=[get_table_of_contents()]
            )
            before_block_id = response.get("results")[0].get("id")
        blocks = []
        sub_contents = []
        l = []
        for content in contents:
            if len(blocks) == 100:
                results = self.append_blocks_to_notion(id, blocks, before_block_id, sub_contents)
                before_block_id = results[-1].get("blockId")
                l.extend(results)
                blocks.clear()
                sub_contents.clear()
                if not self.notion_helper.sync_bookmark and content.get("type")==0:
                    continue
                blocks.append(self.content_to_block(content))
                sub_contents.append(content)
            elif "blockId" in content:
                if len(blocks) > 0:
                    l.extend(
                        self.append_blocks_to_notion(id, blocks, before_block_id, sub_contents)
                    )
                    blocks.clear()
                    sub_contents.clear()
                before_block_id = content["blockId"]
            else:
                if not self.notion_helper.sync_bookmark and content.get("type")==0:
                    continue
                blocks.append(self.content_to_block(content))
                sub_contents.append(content)
        
        if len(blocks) > 0:
            l.extend(self.append_blocks_to_notion(id, blocks, before_block_id, sub_contents))
        for index, value in enumerate(l):
            print(f"正在插入第{index+1}条笔记，共{len(l)}条")
            VipLogManager().add_log(self.vip_id, f"正在插入第{index+1}条笔记，共{len(l)}条")

            if "bookmarkId" in value:
                self.notion_helper.insert_bookmark(id, value)
            elif "reviewId" in value:
                self.notion_helper.insert_review(id, value)
            else:
                self.notion_helper.insert_chapter(id, value)


    def content_to_block(self, content):
        if "bookmarkId" in content:
            return get_block(
                content.get("markText",""),
                self.notion_helper.block_type,
                self.notion_helper.show_color,
                content.get("style"),
                content.get("colorStyle"),
                content.get("reviewId"),
            )
        elif "reviewId" in content:
            return get_block(
                content.get("content",""),
                self.notion_helper.block_type,
                self.notion_helper.show_color,
                content.get("style"),
                content.get("colorStyle"),
                content.get("reviewId"),
            )
        else:
            return get_heading(content.get("level"), content.get("title"))


    def append_blocks_to_notion(self, id, blocks, after, contents):
        response = self.notion_helper.append_blocks_after(
            block_id=id, children=blocks, after=after
        )
        results = response.get("results")
        l = []
        for index, content in enumerate(contents):
            result = results[index]
            if content.get("abstract") != None and content.get("abstract") != "":
                self.notion_helper.append_blocks(
                    block_id=result.get("id"), children=[get_quote(content.get("abstract"))]
                )
            content["blockId"] = result.get("id")
            l.append(content)
        return l
    def __init__(self, weread_api, notion_helper, vip_id):
        self.weread_api = weread_api
        self.notion_helper = notion_helper
        self.vip_id = vip_id
    
    def run(self):
        notion_books = self.notion_helper.get_all_book()
        
        books = self.weread_api.get_notebooklist()
        print(books)
        if books != None:
            for index, book in enumerate(books):
                bookId = book.get("bookId")
                title = book.get("book").get("title")
                sort = book.get("sort")
                if bookId not in notion_books:
                    continue
                if sort == notion_books.get(bookId).get("Sort"):
                    continue
                pageId = notion_books.get(bookId).get("pageId")
                print(f"正在同步《{title}》,一共{len(books)}本，当前是第{index+1}本。")
                VipLogManager().add_log(self.vip_id, f"正在同步《{title}》,一共{len(books)}本，当前是第{index+1}本。")
                chapter = self.weread_api.get_chapter_info(bookId)
                bookmark_list = self.get_bookmark_list(pageId, bookId)
                reviews = self.get_review_list(pageId,bookId)
                bookmark_list.extend(reviews)
                content = self.sort_notes(pageId, chapter, bookmark_list)
                self.append_blocks(pageId, content)
                properties = {
                    "Sort":get_number(sort)
                }
                self.notion_helper.update_book_page(page_id=pageId,properties=properties)

if __name__ == "__main__":
    main()

