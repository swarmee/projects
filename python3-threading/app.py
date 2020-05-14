###
#   gunicorn app:app --reload -b '0.0.0.0:9999' -w 1 -t 300
# 
from queue import Queue
from threading import Thread
import time
from flask  import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

# Set up some global variables
num_fetch_threads = 10
my_work_queue = Queue()

def doFileUploads(i, q):
    while True:
        print("%s: Looking for the next record" % i)
        record = q.get()
        print("%s: Downloading:" % i, record)
        time.sleep(i + 5)
        q.task_done()

for i in range(num_fetch_threads):
    worker = Thread(target=doFileUploads, args=(i, my_work_queue,))
    worker.setDaemon(True)
    worker.start()

@api.route('/queue')
class HelloWorld(Resource):
    def post(self):
        """
        Add a record to the queue
        """
        my_work_queue.put({"data" : "data"})
        return {'message': 'added to work queue'}


@api.route('/queue/count')
class queue_count(Resource):
    def get(self):
        """
        Count the number of records in the queue
        """
        return {'queue_size': my_work_queue.qsize()}

@api.route('/queue/empty')
class queue_count(Resource):
    def get(self):
        """
        Remove everything from the queue
        """
        while my_work_queue.qsize() > 0:
            my_work_queue.get()
            my_work_queue.task_done()
        return {'queue_size': my_work_queue.qsize()}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')
