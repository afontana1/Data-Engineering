from dataclasses import dataclass
import threading
import queue
from typing import Dict, List
import requests


@dataclass
class ThreadRequests(object):
    urls: queue.Queue = queue.Queue()
    infos: queue.Queue = queue.Queue()

    def __init__(
        self,
        urls: List[str],
        http_method: str,
        nb_threads: int = 2,
    ) -> None:
        """Put all urls to the queue url"""
        self.nb_threads = nb_threads
        self.http_method = http_method
        self.workers = {"GET": self.worker_get, "POST": self.worker_post}
        for url in urls:
            self.urls.put(url)

    @property
    def responses(self) -> List[Dict]:
        return list(self.infos.queue)

    def run(self) -> None:
        """Run all workers"""
        for i in range(0, self.nb_threads):
            threading.Thread(target=self.workers[self.http_method], daemon=True).start()
        self.urls.join()

    def worker_get(self) -> None:
        """Pull a url from the queue and make a get request to endpoint"""
        while not self.urls.empty():
            url = self.urls.get()
            resp = requests.get(url)
            self.infos.put(resp.json())
            self.urls.task_done()

    def worker_post(self) -> None:
        """Pull a url from the queue and make a post request to endpoint"""
        while not self.urls.empty():
            url = self.urls.get()
            resp = requests.post(url)
            self.infos.put(resp.json())
            self.urls.task_done()


comments = [
    f"https://jsonplaceholder.typicode.com/comments/{id_}" for id_ in range(1, 500)
]
client = ThreadRequests(comments, "GET", nb_threads=5)
client.run()
