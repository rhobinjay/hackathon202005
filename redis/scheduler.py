from rq import Queue
from rq.job import Job
from worker import conn
from redis import Redis
import time
import pdb

q = Queue(connection=Redis())

def print_message(message):
    with open('msg.txt', 'a') as f:
        f.write(message)
    print(message)
    return len(message)


def run():
    from scheduler import print_message
    job = q.enqueue(print_message, "hello rhobin 1")

run()
