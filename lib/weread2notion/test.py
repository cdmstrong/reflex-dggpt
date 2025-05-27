import os
from notion_client import Client
import requests
from dotenv import load_dotenv
WEREAD_URL = "https://weread.qq.com/"
from urllib.parse import unquote
load_dotenv()
import hashlib
import re
def transform_id(book_id):
    """transform book id to hex string"""
    id_length = len(book_id)
    if re.match(r"^\d*$", book_id):
        ary = []
        for i in range(0, id_length, 9):
            ary.append(format(int(book_id[i : min(i + 9, id_length)]), "x"))
        return "3", ary

    result = ""
    for i in range(id_length):
        result += format(ord(book_id[i]), "x")
    return "4", [result]

def calculate_book_str_id(book_id):
    """calculate book id string"""
    md5 = hashlib.md5()
    md5.update(book_id.encode("utf-8"))
    digest = md5.hexdigest()
    result = digest[0:3]
    code, transformed_ids = transform_id(book_id)
    result += code + "2" + digest[-2:]

    for i in range(len(transformed_ids)):
        hex_length_str = format(len(transformed_ids[i]), "x")
        if len(hex_length_str) == 1:
            hex_length_str = "0" + hex_length_str

        result += hex_length_str + transformed_ids[i]

        if i < len(transformed_ids) - 1:
            result += "g"

    if len(result) < 20:
        result += digest[0 : 20 - len(result)]

    md5 = hashlib.md5()
    md5.update(result.encode("utf-8"))
    result += md5.hexdigest()[0:3]
    print(result)
    return result

def parse_cookie_string(cookie_str):
    cookies = {}
    cookies["Cookie"] = cookie_str
    # for item in cookie_str.split(';'):
    #     if '=' in item:
    #         key, value = item.strip().split('=', 1)
    #         cookies[key] = unquote(value)
    # print(cookies)
    return cookies
from requests.utils import dict_from_cookiejar
# cookies_dict = dict_from_cookiejar(os.environ["WEREAD_COOKIE"])
WEREAD_BOOK_INFO = "https://weread.qq.com/readdata/summary?synckey=0"
# print(cookies_dict) 
session = requests.Session()
session.cookies.update(parse_cookie_string(os.environ["WEREAD_COOKIE"]))
r = session.get(
        url=WEREAD_BOOK_INFO
    )
if r.ok:
    print(r.json())
else:
    errcode = r.json().get("errcode",0)
    # self.handle_errcode(errcode)
    raise Exception(f"Could not get bookshelf {r.text}")
# print(get_bookshelf())