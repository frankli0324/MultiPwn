from multiprocessing import Queue
from time import sleep

from loggers import Board
from flags import FlagHandler
from workers import PwnProcess


class Manager:
    queue = None
    board = None
    job_pool = []
    board_process = None

    @staticmethod
    def init(size=20, try_round=1):
        Manager.queue = Queue()
        Manager.board = Queue()
        Manager.job_pool = [
            PwnProcess(Manager.queue)
            for _ in range(size)
        ]
        [i.start() for i in Manager.job_pool]
        Manager.board_process = Board(
            Manager.board,
            banners=[
                'Round' + str(try_round),
                "|{:^20s}|{:^8s}|{:^10s}|{:^10s}".format(*Job.__keys__)
            ]
        )
        # return
        Manager.board_process.start()

    @staticmethod
    def put(**kwargs):
        if not Manager.job_pool:
            raise EOFError()
        Manager.queue.put(Job(**kwargs))

    @staticmethod
    def terminate():
        while not Manager.queue.empty():
            Manager.queue.get()
        Manager.board_process = None
        [i.terminate() for i in Manager.job_pool]
        Manager.job_pool = None


class Job:
    __keys__ = [
        'target', 'exp', 'status', 'flag',
    ]

    def __init__(self, target, exp):
        # self.id = uuid.uuid4()
        self.flag = 'unknown'
        self.target = target
        self.exp = exp
        self.status = 'starting'
        self.update_status('starting')

    def format(self):
        line = "|{:^20s}|{:^8s}|{:^10s}|{:^10s}".format(
            *[str(getattr(self, i)) for i in self.__keys__]
        )
        return line

    def update_status(self, status):
        self.status = status
        Manager.board.put(self)
        if status == 'starting':
            pass
        elif status == 'submitting':
            self.update_status(FlagHandler.get_result(self.flag))
        elif status == 'attacking':
            pass
        elif status == 'success':
            pass
        elif status == 'error':
            sleep(10)
            self.update_status('submitting')
        elif status == 'wrong':
            sleep(5)
            Manager.put(target=self.target, exp=self.exp)
