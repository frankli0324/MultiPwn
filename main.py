import time

from jobs import Manager
from loader import JobLoader

l = JobLoader('config.yml')
r = 0
try:
    while True:
        r += 1
        Manager.init(try_round=r)
        for exploit, target in l.select(prompt=True):
            Manager.put(target=target, exp=exploit)
        time.sleep(300)  # time after giving another shot
        Manager.terminate()  # terminate the round and start another one
except KeyboardInterrupt:
    Manager.terminate()
