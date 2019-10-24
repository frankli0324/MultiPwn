from multiprocessing import Process


class PwnProcess(Process):
    def __init__(self, work_queue):
        super().__init__()
        self.queue = work_queue

    def run(self):
        while True:
            work = self.queue.get()
            work.update_status('attacking')
            work.flag = __import__(
                'exp.' + work.exp, fromlist=['']
            ).attack(work.target)
            work.update_status('submitting')
