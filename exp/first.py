import random
import time


def attack(target):
    time.sleep(random.randint(1, 9))
    # simulates attack latency
    ip, port = target.split(':')
    return '1\\flag{asdf}'
