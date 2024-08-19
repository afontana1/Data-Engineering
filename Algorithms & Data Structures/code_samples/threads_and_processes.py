import concurrent.futures
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from functools import wraps
from multiprocessing import Pool, cpu_count, Process
from threading import Thread

import requests

BASE_URL = "https://jsonplaceholder.typicode.com/todos/"
NUM_OF_CORES = cpu_count()


def debug(func, prefix="function called: "):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        passed_args = [str(arg) for arg in args]

        if kwargs:
            args_pairs = [f"{arg}={value}" for arg, value in kwargs.items()]
            passed_args.append(", ".join(arg_pair for arg_pair in args_pairs))

        print(
            f"[{elapsed:.6f}s] {prefix} {func.__name__}({', '.join(arg for arg in passed_args)}) "
        )
        return result

    return wrapper


def get_data(id=1):
    start = datetime.now()
    response = requests.get(BASE_URL + str(id))
    print(f"id: {id}, data: {response.json()}")
    return response.json()
    end = datetime.now()
    elapsed = end - start
    print(f"[elapsed {elapsed}]")


@debug
def get_data_by_pool(num_of_workers, num_of_items):
    with Pool(num_of_workers) as p:
        p.map(get_data, range(num_of_items))


@debug
def get_data_sync(num_of_items):
    for id in range(num_of_items):
        get_data(id=id)


@debug
def get_data_by_process(num_of_proc):
    processes = []
    for id in range(num_of_proc):
        p = Process(target=get_data, args=(id,))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


@debug
def get_data_by_threads(num_of_proc):
    threads = []
    for id in range(num_of_proc):
        t = Thread(target=get_data, args=(id,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


@debug
def get_data_by_thread_executor(num_of_items):
    executor = ThreadPoolExecutor(NUM_OF_CORES)
    futures = []
    for i in range(num_of_items):
        future = executor.submit(get_data, i)
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        print(f"result: {future.result()}")


@debug
def get_data_by_process_executor(num_of_items):
    executor = ProcessPoolExecutor(NUM_OF_CORES)
    futures = []
    for i in range(num_of_items):
        future = executor.submit(get_data, i)
        futures.append(future)

    for future in concurrent.futures.as_completed(futures):
        print(f"result: {future.result()}")


def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


@debug
def calculate_fib_by_processes(num_of_proc, n=45):
    processes = []
    for id in range(num_of_proc):
        p = Process(target=fib, args=(n,))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


@debug
def calculate_fib_by_threads(num_of_proc, n=45):
    threads = []
    for id in range(num_of_proc):
        t = Thread(target=fib, args=(n,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    print(f"Detected number of cores: {NUM_OF_CORES}")
    # get_data_by_pool(num_of_workers=NUM_OF_CORES, num_of_items=10)
    get_data_sync(10)
    get_data_by_threads(1000)
    get_data_by_process(10)
    calculate_fib_by_processes(10, n=35)
    calculate_fib_by_threads(10, n=35)
    # get_data_by_thread_executor(10)
    # get_data_by_process_executor(10)
