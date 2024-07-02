# 每x分鐘，跑一次數據
from crontab import CronTab
import os
cron = CronTab(user=True)
path = os.path.abspath("./lesson2.py")
job = cron.new(command=f"/home/pi/miniconda3/bin/python '{path}'")
job.minute.every(10)
job.set_comment("Output hello world")
cron.write()
