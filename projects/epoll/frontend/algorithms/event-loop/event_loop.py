"""
event_loop.py
==================

A tiny "asyncio-like" event loop implemented from scratch using:
- generators/coroutines that **yield** "blocking intents" (Sleep / ReadWait / WriteWait)
- a FIFO queue of runnable tasks
- a min-heap of sleeping tasks (timers)
- OS-backed I/O readiness notification via `selectors`

What this is for
----------------
This is a learning module that demonstrates the core ideas behind cooperative
concurrency and event loops:

1) **Cooperative multitasking**
   Tasks are Python generators. They run until they `yield` an operation
   (e.g., "wait until this socket is readable").

2) **Readiness-based scheduling**
   Instead of blocking the entire process on I/O, tasks yield a request like
   ReadWait(sock). The event loop uses `selectors` to block efficiently until
   the OS reports that the socket is ready.

3) **Timers**
   Tasks can also yield Sleep(delay) to pause themselves. The loop tracks these
   with a heap sorted by wake-up time.

How it compares to real asyncio
-------------------------------
Similarities:
- Tasks represent coroutines
- The loop runs tasks until they yield
- I/O readiness is integrated via a selector
- Timers wake tasks later

Differences (intentional simplifications):
- No Futures/Promises, no await syntax, no cancellation, no exception propagation
  across tasks, no task results, no backpressure, no fairness policies beyond a
  simple queue.
- This loop uses "one-shot" I/O registration: after an fd becomes ready, we
  unregister it immediately and require the task to yield another ReadWait/WriteWait
  if it wants to wait again.
- No cross-thread notifications, no signal handling, no real DNS, etc.

Key mental model
----------------
Each Task alternates between:
- RUNNING (it is in `_ready` and we call `next(coro)`)
- WAITING ON TIMER (it is in `_sleeping` heap)
- WAITING ON I/O (it is registered with `_selector`)

The loop is basically a scheduler that moves tasks between these containers.
"""

from collections import deque
import heapq
import selectors
import time
import socket


# ---------------------------------------------------------------------------
# Yielded "operations" (aka: what a coroutine yields to tell the loop what it
# wants to wait for).
# ---------------------------------------------------------------------------

class ReadWait:
    """
    Operation yielded by a task to indicate:
        "Pause me until `fileobj` is readable."

    `fileobj` must be something the `selectors` module can register
    (typically a socket or file descriptor).
    """
    def __init__(self, fileobj):
        self.fileobj = fileobj


class WriteWait:
    """
    Operation yielded by a task to indicate:
        "Pause me until `fileobj` is writable."

    A common use is non-blocking connect/send: sockets become writable when the
    connect completes or when send buffers have space.
    """
    def __init__(self, fileobj):
        self.fileobj = fileobj


class Sleep:
    """
    Operation yielded by a task to indicate:
        "Pause me for `delay` seconds, then resume."

    Uses a timer heap inside the event loop.
    """
    def __init__(self, delay):
        self.delay = delay  # seconds


# ---------------------------------------------------------------------------
# Task wrapper
# ---------------------------------------------------------------------------

class Task:
    """
    A lightweight wrapper around a generator/coroutine.

    Why wrap?
    ---------
    - We want to attach an ID (useful for tie-breaking in the timer heap).
    - We might later attach more metadata (name, result, exception, etc.).

    Attributes
    ----------
    id : int
        Unique monotonically increasing task ID.
    coro : generator
        The underlying generator-based coroutine.
    """
    _task_id_counter = 0

    def __init__(self, coro):
        Task._task_id_counter += 1
        self.id = Task._task_id_counter
        self.coro = coro  # generator/coroutine


# ---------------------------------------------------------------------------
# Event loop
# ---------------------------------------------------------------------------

class EventLoop:
    """
    A minimal event loop that schedules generator-based tasks.

    Internal queues
    ---------------
    _ready : deque[Task]
        Tasks ready to run *right now* (cooperatively).
    _sleeping : list[tuple[float, int, Task]]
        Min-heap ordered by (wake_time, task_id, task). `task_id` breaks ties.
    _selector : selectors.BaseSelector
        OS-backed mechanism to wait for file descriptors becoming readable/writable.
    _stopped : bool
        Flag to end the loop.

    Scheduling model
    ----------------
    Each iteration of `run_forever()`:
      1) Move expired sleeping tasks into _ready.
      2) If _ready empty: block in selector.select(timeout) waiting for:
         - I/O readiness, or
         - next timer expiry
      3) Run each ready task ONCE (round-robin-ish fairness).
      4) Interpret what the task yielded and move it to the appropriate place:
         - Sleep -> timer heap
         - ReadWait/WriteWait -> selector registration
         - anything else -> put back on _ready

    Notes
    -----
    - This loop uses one-shot I/O registrations: after I/O readiness fires, the fd is
      unregistered and the task is moved back to _ready. If it still needs to wait,
      it must yield ReadWait/WriteWait again.
    - If multiple tasks register the same fileobj simultaneously, `selectors` will raise
      (registration collision). Real loops handle this with more complex bookkeeping.
    """

    def __init__(self):
        self._ready = deque()      # tasks ready to run now
        self._sleeping = []        # heap of (wake_time, task_id, task)
        self._selector = selectors.DefaultSelector()
        self._stopped = False

    # ---- public API ----

    def create_task(self, coro):
        """
        Schedule a coroutine to be run by the loop.

        Parameters
        ----------
        coro : generator
            A generator-based coroutine that yields operation objects (Sleep, ReadWait, WriteWait).

        Returns
        -------
        Task
            The created Task wrapper.

        Behavior
        --------
        The task is appended to the _ready queue and will run on the next loop iteration.
        """
        task = Task(coro)
        self._ready.append(task)
        return task

    def stop(self):
        """
        Request the loop to stop after the current iteration.

        This simply flips a flag. The loop checks `_stopped` at the top of the
        `while` loop in `run_forever()`.
        """
        self._stopped = True

    def run_forever(self):
        """
        Run tasks, manage timers & I/O, until `stop()` is called or no work remains.

        Exit conditions
        ---------------
        - `_stopped` becomes True (via stop()).
        - There are no runnable tasks, no timers, and no registered I/O watchers.

        Important detail: "Run all tasks that are ready once each"
        ----------------------------------------------------------
        We compute `n_ready = len(_ready)` and then pop/run that many tasks.
        If tasks re-queue themselves during this pass, they will generally run
        in the *next* loop iteration. This provides a simple fairness mechanism
        and prevents a single task from starving others by repeatedly yielding
        "run again".
        """
        while not self._stopped:
            # 1) Wake up any timers that have expired
            self._wake_sleepers()

            # 2) If nothing is ready, block waiting for I/O or next timer
            if not self._ready:
                timeout = None

                # If we have sleeping tasks, compute how long until the next one
                if self._sleeping:
                    timeout = max(0, self._sleeping[0][0] - time.monotonic())

                # If we have I/O watchers or a timer deadline, we can block efficiently
                if self._selector.get_map() or timeout is not None:
                    events = self._selector.select(timeout)
                    for key, mask in events:
                        task = key.data  # we stored the waiting Task in selector data

                        # One-shot registration:
                        # Once it fires, unregister and make task runnable again.
                        self._selector.unregister(key.fileobj)
                        self._ready.append(task)

                    # Timers might have expired during the wait
                    self._wake_sleepers()
                else:
                    # No tasks, no timers, no I/O: nothing more to do
                    break

            # 3) Run all tasks that are ready *once each*
            n_ready = len(self._ready)
            for _ in range(n_ready):
                task = self._ready.popleft()

                try:
                    # Advance the coroutine until it yields an operation
                    op = next(task.coro)
                except StopIteration:
                    # Task finished: drop it (no re-scheduling)
                    continue

                # 4) Interpret what the task yielded and schedule accordingly
                if isinstance(op, Sleep):
                    self._schedule_sleep(task, op.delay)
                elif isinstance(op, ReadWait):
                    self._schedule_io(task, op.fileobj, selectors.EVENT_READ)
                elif isinstance(op, WriteWait):
                    self._schedule_io(task, op.fileobj, selectors.EVENT_WRITE)
                else:
                    # Unknown yield type -> treat as "yield control, run me again later"
                    self._ready.append(task)

    # ---- internal helpers ----

    def _schedule_sleep(self, task, delay):
        """
        Put `task` to sleep for `delay` seconds.

        Uses a min-heap so we can efficiently find the next task that should wake.
        Heap entries are (wake_time, task.id, task) so that:
        - earliest wake_time pops first
        - task.id provides deterministic ordering for ties
        """
        when = time.monotonic() + delay
        heapq.heappush(self._sleeping, (when, task.id, task))

    def _schedule_io(self, task, fileobj, events):
        """
        Register `task` to be resumed when `fileobj` is ready for `events`.

        Parameters
        ----------
        fileobj : socket/file-like
            Must be compatible with selectors (has fileno()).
        events : int
            selectors.EVENT_READ or selectors.EVENT_WRITE

        Notes
        -----
        This is "one-shot": the registration is removed once it fires.
        If a task needs to wait again, it must yield another ReadWait/WriteWait.
        """
        self._selector.register(fileobj, events, task)

    def _wake_sleepers(self):
        """
        Move any sleeping tasks whose wake_time has arrived into the ready queue.

        Complexity
        ----------
        Each awakened task is popped from the heap once: O(log n) per wake-up.
        """
        now = time.monotonic()
        while self._sleeping and self._sleeping[0][0] <= now:
            _, _, task = heapq.heappop(self._sleeping)
            self._ready.append(task)


# ---------------------------------------------------------------------------
# Example application: echo server + client running on the custom loop
# ---------------------------------------------------------------------------

def echo_server(sock, loop):
    """
    Coroutine: accept incoming connections and spawn a handler per client.

    Flow
    ----
    1) Yield ReadWait(listening_socket): pause until a new connection is ready to accept.
    2) accept() the connection (non-blocking socket).
    3) create a new task handle_client(conn, loop) to echo data.
    4) loop forever.

    Notes
    -----
    - The listening socket must be non-blocking, or accept() could block the whole process.
    - This coroutine never returns; it runs until the loop is stopped externally.
    """
    while True:
        # Wait until the listening socket is readable (incoming connection pending)
        yield ReadWait(sock)

        conn, addr = sock.accept()
        conn.setblocking(False)
        print("server: accepted", addr)

        # Spawn a new coroutine to handle this client
        loop.create_task(handle_client(conn, loop))


def handle_client(conn, loop):
    """
    Coroutine: echo back everything the client sends until it closes.

    Flow
    ----
    1) Yield ReadWait(conn): pause until the client socket is readable.
    2) recv() data (may raise BlockingIOError if not actually ready yet).
    3) If recv returns b"" -> client closed, close socket and return (task ends).
    4) Yield WriteWait(conn): pause until socket is writable.
    5) sendall(data) back to the client.

    Notes
    -----
    - In real-world non-blocking code, you'd typically handle partial sends and
      readiness loops more carefully.
    - This example keeps logic simple for learning purposes.
    """
    while True:
        # Wait for data from client
        yield ReadWait(conn)

        try:
            data = conn.recv(1024)
        except BlockingIOError:
            # OS said "readable" but we still couldn't read (rare but possible).
            # Just try again.
            continue

        if not data:
            print("server: client closed")
            conn.close()
            return

        print("server: got", data)

        # Wait until socket is writable, then send
        yield WriteWait(conn)
        try:
            conn.sendall(data)
        except BlockingIOError:
            # If send buffers are full, wait again for writable.
            yield WriteWait(conn)


def client_task(addr, loop):
    """
    Coroutine: connect to the server, send a message, receive echo, then stop loop.

    Demonstrates non-blocking connect:
    - connect() on a non-blocking socket usually raises BlockingIOError, meaning:
        "connection in progress"
    - sockets are typically considered writable when the connection completes

    Flow
    ----
    1) Create non-blocking socket, initiate connect.
    2) Yield WriteWait(socket): wait until connect completes.
    3) Send message.
    4) Yield ReadWait(socket): wait for echo.
    5) Print result, close socket, stop event loop.
    """
    s = socket.socket()
    s.setblocking(False)

    try:
        s.connect(addr)
    except BlockingIOError:
        # Non-blocking connect in progress
        pass

    # Wait until connection is established (socket writable)
    yield WriteWait(s)
    s.sendall(b"hello from client")

    # Wait for response
    yield ReadWait(s)
    data = s.recv(1024)
    print("client got:", data)
    s.close()

    # Stop the event loop once we're done (so the script terminates)
    loop.stop()


if __name__ == "__main__":
    """
    Demo: run an echo server and a client within the same process/event loop.

    - Create a listening socket on 127.0.0.1 with an ephemeral port (port=0).
    - Spawn an echo_server task to accept and handle clients.
    - Spawn a client_task that connects, sends one message, receives echo, stops loop.
    - Run the loop.

    Expected output resembles:
      server: accepted ('127.0.0.1', 12345)
      server: got b'hello from client'
      client got: b'hello from client'
      server: client closed
    """
    # Create listening socket
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", 0))  # random free port
    server_sock.listen()
    server_sock.setblocking(False)
    addr = server_sock.getsockname()

    loop = EventLoop()
    loop.create_task(echo_server(server_sock, loop))
    loop.create_task(client_task(addr, loop))
    loop.run_forever()