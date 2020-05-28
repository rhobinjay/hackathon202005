import os
import redis
import pdb
from rq import Worker, Queue, Connection
from rq.registry import StartedJobRegistry

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

def main():
    with Connection(conn):
#        queue = Queue(connection=conn)
#        for job_id in queue.job_ids:
#            queue.fetch_job(job_id)
#        if queue:
#            
#            queue.fetch
        queue = Queue(connection=conn)
        registry = StartedJobRegistry(queue=queue)
        pdb.set_trace()
        worker = Worker(list(map(Queue, listen)))
        worker.work()

if __name__ == '__main__':
    main()

