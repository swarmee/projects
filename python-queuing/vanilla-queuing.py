from queue import Queue
import time
from threading import Thread
import requests
import pendulum

totalRunTime = []


def do_stuff(q):
    while True:
        global totalRunTime
        print(Queue.qsize(q))
        startTime = pendulum.now()
        res = requests.get('https://pokeapi.co/api/v2/ability/150/')
        endTime = pendulum.now()
        print('item : ' + str(q.get()) + '  runTime: ' +
              str(endTime.diff(startTime).in_seconds()))
        time.sleep(2)
        totalRunTime.append(endTime.diff(startTime).in_seconds())
        q.task_done()


q = Queue(maxsize=0)
num_threads = 2

for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q, ))
    worker.setDaemon(True)
    worker.start()

for x in range(7):
    q.put(x)

q.join()

print(totalRunTime)
