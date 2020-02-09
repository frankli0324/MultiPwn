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
            loggers=[ConsoleLogger(), FileLogger()]
        )
        for exploit, target in l.select():
            Manager.put(target=target, exp=exploit)
        time.sleep(300)  # time after giving another shot
        Manager.terminate()  # terminate the round and start another one
except KeyboardInterrupt:
    Manager.terminate()
