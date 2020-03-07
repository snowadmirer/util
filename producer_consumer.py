from multiprocessing import Queue, Process

def producer(queue):
    for i in range(100000):
        queue.put(i)

def consumer(queue):
    while True:
        try:
            i = queue.get(timeout=60)
        except Exception as e:
            print(e)
            break
if __name__ == '__main__'
    queue = Queue(500)
    procs = []
    producer_proc = Process(target=producer, args=(queue,))
    producer_proc.start()
    procs.append(producer_proc)
    consumer_num = 10
    for i in range(consumer_num):
        consumer_proc = Process(target=consumer, args=(queue,))
        consumer_proc.start()
        procs.append(consumer_proc)
    for proc in procs:
        proc.join()
        
