#coding=utf-8
from multiprocessing import Queue, Event, Process
from random import randint

def producer(queue, event):
    while True:
        num = randint(0, 10)
        print('producing {}'.format(num))
        queue.put(num)
        if event.is_set():
            print('producer exit')
            break

if __name__ == '__main__':
    queue = Queue(maxsize=10)
    event = Event()
    print(dir(event))
    Process(target=producer, args=(queue, event)).start()
    for i in range(100):
        num = queue.get()
        print('consuming {}'.format(num))
    event.set()
