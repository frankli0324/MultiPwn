#!--encoding=utf-8--

import time

from jobs import Manager
from loader import JobLoader
from submitters import *
from loggers import *

l = JobLoader('config.yml')
try:
    while True:
        Manager.init(
            flag_submitter=CTFdSubmitter('http://localhost:4000', 'test', 'test'),
            loggers=[ConsoleLogger()],  # , FileLogger()
            # 由于运行中会产生大量输出，尽量不要用FileLogger
            workers=50
            # 尽量保证workers数大于等于target数乘exploit数，不然**看上去**会特别卡
        )
        for exploit, target in l.select():
            Manager.put(target=target, exp=exploit)
        time.sleep(300)  # 每轮间隔
        Manager.terminate()
except KeyboardInterrupt:
    Manager.terminate()
