# python3
from collections import namedtuple

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])
# Task. You have a program which is parallelized and uses 𝑛 independent threads to process the given list of 𝑚
# jobs. Threads take jobs in the order they are given in the input. If there is a free thread, it immediately
# takes the next job from the list. If a thread has started processing a job, it doesn’t interrupt or stop
# until it finishes processing the job. If several threads try to take jobs from the list simultaneously, the
# thread with smaller index takes the job. For each job you know exactly how long will it take any thread
# to process this job, and this time is the same for all the threads. You need to determine for each job
# which thread will process it and when will it start processing.
# The first line of the input contains integers n and m.
# The second line contains m integers t[i] — the times in seconds it takes any thread to process i-th job.
# The times are given in the same order as they are in the list from which threads take jobs.
# Threads are indexed starting from 0.
# Output Format. Output exactly m lines. i-th line (0-based index is used) should contain two spaceseparated
# integers — the 0-based index of the thread which will process the i-th job and the time
# in seconds when it will start processing that job.


class Heap:  # A modified binary heap
    def __init__(self, arr):
        # At the beginning, no thread is assigned to any job and starting time for each job is 0 (ready to do at immediately)
        self.arr = arr  # Input array: stores the starting time for each thread
        self.thread = [
            i for i in range(len(arr))
        ]  # record the index of threads responsible for each thread

    def LeftChild(i):
        return 2 * i + 1

    def RightChild(i):
        return 2 * i + 2

    def GetMin(self):
        return (
            self.arr[0],
            self.thread[0],
        )  # Return the thread that is the earlist available and its starting time for the new job

    def ChangePriority(self, p):
        self.arr[
            0
        ] += p  # Update the starting time for processing when new job is added
        Heap.SiftDown(self, 0)  # Maintain the heap structure

    def SiftDown(self, i):
        minIndex = i
        l = Heap.LeftChild(i)
        if l < len(self.arr):
            if (
                self.arr[l] < self.arr[minIndex]
            ):  # Find the thread with smaller starting time (avilable earlier)
                minIndex = l
            if (self.arr[l] == self.arr[minIndex]) & (
                self.thread[l] < self.thread[minIndex]
            ):  # If it happens that two threads are available at the same time, find the thread with smaller index
                minIndex = l
        r = Heap.RightChild(i)
        if r < len(self.arr):
            if (
                self.arr[r] < self.arr[minIndex]
            ):  # Find the thread with smaller starting time (avilable earlier)
                minIndex = r
            if (self.arr[r] == self.arr[minIndex]) & (
                self.thread[r] < self.thread[minIndex]
            ):  # If it happens that two threads are available at the same time, find the thread with smaller index
                minIndex = r
        if (
            i != minIndex
        ):  # Sift the current thread (which received new job and expected to be available later) down and push the earliest available thread to the root
            self.arr[i], self.arr[minIndex] = self.arr[minIndex], self.arr[i]
            self.thread[i], self.thread[minIndex] = (
                self.thread[minIndex],
                self.thread[i],
            )
            Heap.SiftDown(self, minIndex)


def pq_assign_jobs(n_workers, jobs):
    result = []
    next_free_time_heap = Heap([0] * n_workers)  # A heap of thread status
    for i in range(len(jobs)):
        (
            next_free_time,
            next_worker,
        ) = (
            next_free_time_heap.GetMin()
        )  # First job can always be processed immediately
        result.append(AssignedJob(next_worker, next_free_time))
        next_free_time_heap.ChangePriority(
            jobs[i]
        )  # Update thread status for each new coming job, jobs[i] stores the time to process the (i + 1)-th job
    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = pq_assign_jobs(n_workers, jobs)
    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
