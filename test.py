
from datetime import datetime
import re

from matplotlib.dates import relativedelta

def invalid_email(email: str) -> bool:
    # 定义邮箱的正则表达式
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
    # 使用 re.match 方法进行匹配
    if re.match(pattern, email):
        return True
    else:
        return False

if __name__ == "__main__":
    print(invalid_email("23213@qq.com"))
    print(invalid_email("2321.com"))
