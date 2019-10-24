import time
from yaml import safe_load
from job_manager import Manager

exps = safe_load(open('config.yml', 'r'))
r = 0
while True:
    r += 1
    Manager.init(try_round=r)
    for exp in exps['root']:
        for target in exp['targets']:
            Manager.put(target=target, exp=exp['name'])
    time.sleep(300)  # time after giving another shot
    Manager.terminate()  # terminate the round and start another one
