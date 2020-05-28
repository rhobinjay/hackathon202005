from rq import Queue
from rq.job import Job
from worker import conn
import time
import pdb

q = Queue(connection=conn)

def print_message(message):
    with open('msg.txt', 'a') as f:
        f.write(message)
    print(message)
    return


def run():
    from scheduler import print_message

    job = q.enqueue(print_message, args=("hello rhobin 1",), result_ttl=0)
    job = q.enqueue(print_message, args=("hello rhobin 2",), result_ttl=0)

run()
