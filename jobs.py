from importlib import import_module
from multiprocessing import Process
from multiprocessing import Queue
from time import sleep

from loggers import Logger


class Manager:
    job_queue = None
    log_queue = None
    job_pool = []
    logger_process = None
    submitter = None

    @staticmethod
    def init(flag_submitter, loggers, workers=20):
        Manager.job_queue = Queue()
        Manager.log_queue = Queue()
        Manager.submitter = flag_submitter
        Manager.job_pool = [
            JobConsumer(Manager.job_queue)
            for _ in range(workers)
        ]
        [i.start() for i in Manager.job_pool]
        Manager.logger_process = Logger(
            Manager.log_queue, *loggers
        )
        # return
        Manager.logger_process.start()

    @staticmethod
    def log(obj): # Job instance
        Manager.log_queue.put(obj)

    @staticmethod
    def put(**kwargs):
        if not Manager.job_pool:
            raise EOFError()
        Manager.job_queue.put(Job(**kwargs))
    
    @staticmethod
    def submit(answer):
        return Manager.submitter.submit(answer)

    @staticmethod
    def terminate():
        while not Manager.job_queue.empty():
            Manager.job_queue.get()
        Manager.logger_process = None
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

    def update_status(self, status):
        self.status = status
        Manager.log(self)
        if status == 'starting':
            pass
        elif status == 'submitting':
            try:
                self.update_status(
                    Manager.submit(self.flag)
                )
            except:
                self.update_status('submit_error')
        elif status == 'attacking':
            pass
        elif status == 'success':
            pass
        elif status == 'submit_error':
            sleep(10)
            self.update_status('submitting')
        elif status == 'wrong' or status == 'exploit_error':
            sleep(5)
            Manager.put(target=self.target, exp=self.exp)


class JobConsumer(Process):
    def __init__(self, work_queue):
        super(JobConsumer, self).__init__()
        self.queue = work_queue

    def run(self):
        try:
            while True:
                work = self.queue.get()
                work.update_status('attacking')
                try:
                    work.flag = import_module(
                        '.' + work.exp, 'exp'
                    ).attack(work.target)
                except:
                    work.update_status('exploit_error')
                    continue
                work.update_status('submitting')
        except KeyboardInterrupt:
            pass
