# Python3
import time
import random
import asyncio
from concurrent.futures import ProcessPoolExecutor

import multiprocessing
import time


class ConcurrentProcessing:
    _lock = None
    _name = ''
    _loop = asyncio.get_event_loop()
    _executor = ProcessPoolExecutor()

    def __init__(self, class_lock, class_name):
        if ConcurrentProcessing._lock is None:
            ConcurrentProcessing._lock = class_lock
        self._name = class_name
        self._lock = ConcurrentProcessing._lock

    def worker(self, uid, p_lock, no_iterations):
        calculation = 0
        for i in range(no_iterations):
            calculation += random.randint(-1, 1)

        lock_acquired = False
        while not lock_acquired:
            lock_acquired = p_lock.acquire(False)
            if lock_acquired:
                print(type(self).__name__, 'class name', self._name, 'process id', uid,
                      '(base class definition) entering locked area, calculation is:', calculation)
            else:
                time.sleep(random.randint(1, 2) / 4.0)
        p_lock.release()

    async def process(self, no_workers, p_lock, no_iterations):
        tasks = []
        for uid in range(no_workers):
            tasks.append(self._loop.run_in_executor(self._executor, self.worker, uid, p_lock, no_iterations))
        await asyncio.gather(*tasks)

    def run(self, no_workers, p_lock, no_iterations):
        print(type(self).__name__, '(base class definition) run method')
        self._loop.run_until_complete(self.process(no_workers=no_workers, p_lock=p_lock, no_iterations=no_iterations))


# usage, derive your class from ConcurrentProcessing
# overwrite the methods worker, process, and run as required
if __name__ == '__main__':
    # call required for running on Windows
    multiprocessing.freeze_support()

    no_workers = 50
    no_iterations = 100000

    start_time = time.time()
    log_processing = ConcurrentProcessing(class_lock=multiprocessing.Manager().Lock(), class_name='log_processing_1')
    log_processing.run(no_workers=no_workers, p_lock=multiprocessing.Manager().Lock(), no_iterations=no_iterations)

    print("--- %s seconds ---" % (time.time() - start_time))
