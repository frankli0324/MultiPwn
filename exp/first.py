import random
import time


def attack(target: str):
    time.sleep(random.randint(1, 9))
    # simulates attack latency
    ip, port = target.split(':')
    return f'flag{{{random.randint(999, 7000)}}}'
