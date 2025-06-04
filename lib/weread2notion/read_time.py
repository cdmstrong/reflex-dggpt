from datetime import datetime
from datetime import timedelta
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pendulum

from .weread_api import WeReadApi
from .notion_helper import NotionHelper
from .utils import (
    format_date,
    get_date,
    get_icon,
    get_number,
    get_relation,
    get_title,
)
from dotenv import load_dotenv
HEATMAP_GUIDE = "https://mp.weixin.qq.com/s?__biz=MzI1OTcxOTI4NA==&mid=2247484145&idx=1&sn=81752852420b9153fc292b7873217651&chksm=ea75ebeadd0262fc65df100370d3f983ba2e52e2fcde2deb1ed49343fbb10645a77570656728&token=157143379&lang=zh_CN#rd"

load_dotenv()

class Read_time():

    def insert_to_notion(self, page_id, timestamp, duration):
        parent = {"database_id": self.notion_helper.day_database_id, "type": "database_id"}
        properties = {
            "标题": get_title(
                format_date(
                    datetime.utcfromtimestamp(timestamp) + timedelta(hours=8),
                    "%Y年%m月%d日",
                )
            ),
            "日期": get_date(
                start=format_date(datetime.utcfromtimestamp(timestamp) + timedelta(hours=8))
            ),
            "时长": get_number(duration),
            "时间戳": get_number(timestamp),
            "年": get_relation(
                [
                    self.notion_helper.get_year_relation_id(
                        datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
                    ),
                ]
            ),
            "月": get_relation(
                [
                    self.notion_helper.get_month_relation_id(
                        datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
                    ),
                ]
            ),
            "周": get_relation(
                [
                    self.notion_helper.get_week_relation_id(
                        datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
                    ),
                ]
            ),
        }
        if page_id != None:
            self.notion_helper.client.pages.update(page_id=page_id, properties=properties)
        else:
            self.notion_helper.client.pages.create(
                parent=parent,
                icon=get_icon("https://www.notion.so/icons/target_red.svg"),
                properties=properties,
            )


    def get_file(self):
        # 设置文件夹路径
        folder_path = "./OUT_FOLDER"

        # 检查文件夹是否存在
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            entries = os.listdir(folder_path)

            file_name = entries[0] if entries else None
            return file_name
        else:
            print("OUT_FOLDER does not exist.")
            return None


    def __init__(self, weread_api, notion_helper, vip_id):
        self.notion_helper = notion_helper
        self.weread_api = weread_api
        self.vip_id = vip_id
    def run(self):
        # image_file = self.get_file()
        # if image_file:
        #     image_url = f"https://raw.githubusercontent.com/{os.getenv('REPOSITORY')}/{os.getenv('REF').split('/')[-1]}/OUT_FOLDER/{image_file}"
        #     heatmap_url = f"https://heatmap.malinkang.com/?image={image_url}"
        #     if self.notion_helper.heatmap_block_id:
        #         response = self.notion_helper.update_heatmap(
        #             block_id=self.notion_helper.heatmap_block_id, url=heatmap_url
        #         )
        #     else:
        #         print(f"更新热力图失败，没有添加热力图占位。具体参考：{HEATMAP_GUIDE}")
        # else:
        #     print(f"更新热力图失败，没有生成热力图。具体参考：{HEATMAP_GUIDE}")
        api_data = self.weread_api.get_api_data()
        readTimes = {int(key): value for key, value in api_data.get("readTimes").items()}
        now = pendulum.now("Asia/Shanghai").start_of("day")
        today_timestamp = now.int_timestamp
        if today_timestamp not in readTimes:
            readTimes[today_timestamp] = 0
        readTimes = dict(sorted(readTimes.items()))
        results = self.notion_helper.query_all(database_id=self.notion_helper.day_database_id)
        for result in results:
            timestamp = result.get("properties").get("时间戳").get("number")
            duration = result.get("properties").get("时长").get("number")
            id = result.get("id")
            if timestamp in readTimes:
                value = readTimes.pop(timestamp)
                if value != duration:
                    self.insert_to_notion(page_id=id, timestamp=timestamp, duration=value)
        for key, value in readTimes.items():
            self.insert_to_notion(None, int(key), value)
if __name__ == "__main__":
    main()
