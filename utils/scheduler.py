from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APSchedulerManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("APScheduler 已启动")

    def add_cron_job(self, func, job_id, hour=0, minute=0, second=0, **kwargs):
        """
        添加一个基于 cron 的定时任务。
        :param func: 要执行的函数
        :param job_id: 任务 ID，必须唯一
        :param hour: 小时
        :param minute: 分钟
        :param second: 秒
        :param kwargs: 传递给函数的关键字参数
        """
        try:
            trigger = CronTrigger(hour=hour, minute=minute, second=second)
            self.scheduler.add_job(func, trigger, id=job_id, kwargs=kwargs, replace_existing=True)
            logger.info(f"添加任务成功: {job_id}")
        except Exception as e:
            logger.error(f"添加任务失败: {e}")

    def remove_job(self, job_id):
        """
        移除指定 ID 的任务。
        :param job_id: 任务 ID
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"移除任务成功: {job_id}")
        except JobLookupError:
            logger.warning(f"任务不存在: {job_id}")

    def pause_job(self, job_id):
        """
        暂停指定 ID 的任务。
        :param job_id: 任务 ID
        """
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"暂停任务成功: {job_id}")
        except JobLookupError:
            logger.warning(f"任务不存在: {job_id}")

    def resume_job(self, job_id):
        """
        恢复指定 ID 的任务。
        :param job_id: 任务 ID
        """
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"恢复任务成功: {job_id}")
        except JobLookupError:
            logger.warning(f"任务不存在: {job_id}")

    def list_jobs(self):
        """
        列出所有已添加的任务。
        """
        jobs = self.scheduler.get_jobs()
        if not jobs:
            logger.info("当前没有任务")
        for job in jobs:
            logger.info(f"任务 ID: {job.id}, 下次运行时间: {job.next_run_time}")

SchedulerManager = APSchedulerManager()