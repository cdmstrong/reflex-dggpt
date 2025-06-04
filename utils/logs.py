# 用于存储vip的运行日志信息
# 每个vip的任务id，存储一个运行日志，为字符串格式，最好为单例模型，方便进行日志的存储和读取
import os

from pydantic import BaseModel 

class VipLog(BaseModel):
    task_id: int
    log: str

# 单例装饰器
def singleton(cls):
    _instance = {}
    def wrapper(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper

@singleton
class VipLogManager:
    logs = {}

    def add_log(self, task_id: int, log: str):
        if task_id not in self.logs:
            self.logs[task_id] = VipLog(task_id=task_id, log=log)
        else:
            self.logs[task_id].log += f"\n{log}"

    def get_log(self, task_id: int):
        if task_id not in self.logs:
            return ""
        return self.logs[task_id].log

    def delete_log(self, task_id: int):
        self.logs.pop(task_id, None)

    def get_all_logs(self):
        return self.logs


if __name__ == "__main__":
    vip_log_manager = VipLogManager()
    vip_log_manager.add_log("1", "test")
    vip_log_manager.add_log("1", "test")
    vip_log_manager1 = VipLogManager()
    print(vip_log_manager.get_log("1"))
    print(vip_log_manager.get_all_logs())
