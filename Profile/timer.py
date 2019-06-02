import time

def start_time() :
    timer = time.time()
    return timer

def end_time(start) :
    end = time.time()
    timer = end - start
    return timer