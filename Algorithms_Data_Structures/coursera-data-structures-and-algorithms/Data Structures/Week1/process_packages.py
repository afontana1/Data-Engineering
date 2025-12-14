# python3
from collections import namedtuple, deque

Request = namedtuple("Request", ["arrived_at", "time_to_process"])
Response = namedtuple("Response", ["was_dropped", "started_at"])
# Input Format. The first line of the input contains the size S of the buffer and the number n of incoming
# network packets. Each of the next n lines contains two numbers. i-th line contains the time of arrival
# A[i] and the processing time P[i] (both in milliseconds) of the i-th packet. It is guaranteed that the
# sequence of arrival times is non-decreasing (however, it can contain the exact same times of arrival in
# milliseconds — in this case the packet which is earlier in the input is considered to have arrived earlier).
# Output Format. For each packet output either the moment of time (in milliseconds) when the processor
# began processing it or −1 if the packet was dropped (output the answers for the packets in the same
# order as the packets are given in the input).


class Buffer:
    def __init__(self, size):
        self.size = size  # Buffer size
        self.finish_time = deque()  # Let finish time be a double queue

    def process(self, request):
        if (
            len(self.finish_time) == 0
        ):  # If finish_time is empty queue, then it is ready to accept any requests
            est_finish_time = (
                request.arrived_at + request.time_to_process
            )  # Estimated finish time = Arrival time + Time to process the request
            self.finish_time.append(est_finish_time)
            return Response(
                False, request.arrived_at
            )  # So, the request will be processed at arrival time
        else:  # Otherwise, there are some requests not processed in the queue
            act_finish_time = self.finish_time[0]
            if (
                act_finish_time <= request.arrived_at
            ):  # If the first request can be finished before the arrival of the current request, pop it
                self.finish_time.popleft()
            if (
                len(self.finish_time) == 0
            ):  # If it is an empty list after the first request is popped, repeat the previous process for empty queue
                est_finish_time = request.arrived_at + request.time_to_process
                self.finish_time.append(est_finish_time)
                return Response(False, request.arrived_at)
            else:  # Otherwise, the queue has at least 2 requests before popping out the 1 request
                prev_finish_time = self.finish_time[-1]
                if (
                    prev_finish_time > request.arrived_at
                ):  # If the last request cannot be finished before the current request arrives and we have space to accomodate an extra request
                    if self.size > len(self.finish_time):
                        self.finish_time.append(
                            prev_finish_time + request.time_to_process
                        )  # then add to the buffer list and it will be processed when the last request is finished
                        return Response(False, prev_finish_time)
                else:  # If the last request can be finishe before the current request arrives and we have space to accomodate an extra request
                    if self.size > len(self.finish_time):
                        self.finish_time.append(
                            request.arrived_at + request.time_to_process
                        )  # then add to the buffer list and it will be processed as soon as it arrives
                        return Response(False, request.arrived_at)
            return Response(
                True, request.arrived_at
            )  # Otherwise, it must be the case that buffer size is fulled when an extra request comes, and it will be dropped


def process_requests(requests, buffer):
    responses = []
    for request in requests:
        responses.append(buffer.process(request))  # Process request one by one
    return responses


def main():
    buffer_size, n_requests = map(int, input().split())
    requests = []
    for _ in range(n_requests):
        arrived_at, time_to_process = map(
            int, input().split()
        )  # Read arrival time and time to process for each request and store them as a Request object in requests list.
        requests.append(Request(arrived_at, time_to_process))
    buffer = Buffer(buffer_size)  # A Buffer object with size of buffer_size
    responses = process_requests(requests, buffer)  # Get response from requests

    for response in responses:
        print(response.started_at if not response.was_dropped else -1)


if __name__ == "__main__":
    main()
