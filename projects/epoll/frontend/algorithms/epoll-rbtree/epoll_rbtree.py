"""
epoll_rb.py
===========

A **toy**, user-space, epoll-like interface backed by a Red–Black Tree.

What this is for
----------------
This file demonstrates (conceptually) how an *interest set* and a *ready list*
can be represented in user space:

- **Interest set**: "which file descriptors (fd) am I watching, and for what events?"
  Implemented here as an RBTree keyed by fd.
- **Ready queue**: "which fds are currently ready, and what happened?"
  Implemented here as a FIFO deque.

This is *not* a real epoll implementation:
- There is no kernel integration, no OS file descriptors, no interrupts.
- Readiness is simulated via `trigger(...)`.
- `wait(...)` is a simple polling loop.

Why RBTree?
-----------
Linux epoll internally needs an efficient structure to store registered fds and
support fast add/remove/lookup. A balanced tree gives O(log n) operations and keeps
the interest set ordered by key. This example uses an RBTree to mimic that idea.

Data model
----------
The RBTree stores:
    fd -> {"events": event_mask, "data": user_data}

The ready queue stores tuples:
    (fd, event_mask, user_data)

Note: `event_mask` is a bitmask (e.g., EPOLLIN | EPOLLOUT).
"""

from collections import deque
import time

from rbtree import RBTree


class EpollRB:
    """
    Toy epoll-like object using an RBTree for the interest set.

    Methods map loosely to Linux epoll:
    - register(fd, events, data): like epoll_ctl(EPOLL_CTL_ADD)
    - modify(fd, events, data):   like epoll_ctl(EPOLL_CTL_MOD)
    - unregister(fd):             like epoll_ctl(EPOLL_CTL_DEL)
    - wait(timeout, maxevents):   like epoll_wait()
    - trigger(fd, event_mask):    *simulation hook* (kernel would do this in reality)

    Internal state
    --------------
    _tree : RBTree
        Stores the interest set: fd -> {"events": ..., "data": ...}
    _ready : deque
        FIFO queue of ready notifications as (fd, event_mask, data).
    """

    def __init__(self):
        """
        Create an empty EpollRB instance.

        Starts with:
        - empty interest set (RBTree)
        - empty ready queue (deque)
        """
        self._tree = RBTree()
        self._ready = deque()

    def register(self, fd, events, data=None):
        """
        Register a file descriptor in the interest set.

        Parameters
        ----------
        fd : int
            Identifier for the watched object (in real life: OS file descriptor).
        events : int
            Bitmask of events the caller is interested in (e.g., EPOLLIN|EPOLLOUT).
        data : any, optional
            Arbitrary user payload to return back when the fd is reported ready.

        Behavior
        --------
        - If fd is new: inserts it.
        - If fd already exists: overwrites its events/data (simple behavior for a toy).

        Complexity
        ----------
        O(log n) due to RBTree insert/update.
        """
        self._tree.insert(fd, {"events": events, "data": data})

    def modify(self, fd, events, data=None):
        """
        Modify an existing registration.

        Parameters
        ----------
        fd : int
            Previously-registered fd to update.
        events : int
            New event interest mask.
        data : any, optional
            New user payload.

        Raises
        ------
        KeyError
            If fd is not registered.

        Complexity
        ----------
        O(log n) for RBTree search.
        """
        node = self._tree.search(fd)
        if node is None:
            raise KeyError(f"fd {fd} not registered")
        node.value["events"] = events
        node.value["data"] = data

    def unregister(self, fd):
        """
        Remove an fd from the interest set.

        Parameters
        ----------
        fd : int
            fd to remove.

        Raises
        ------
        KeyError
            If fd is not registered.

        Complexity
        ----------
        O(log n) for RBTree delete.
        """
        if not self._tree.delete(fd):
            raise KeyError(f"fd {fd} not registered")

    def trigger(self, fd, event_mask):
        """
        Simulation hook: mark an fd as having events ready.

        In a real OS:
        - the kernel would detect readiness (via interrupts, polling, driver callbacks),
          then enqueue readiness notifications internally.
        - user code would call epoll_wait() to retrieve them.

        Here:
        - `trigger` plays the role of "the kernel noticing something happened".

        Parameters
        ----------
        fd : int
            fd that became ready.
        event_mask : int
            Bitmask describing what became ready (e.g., EPOLLIN).

        Behavior
        --------
        - If fd is not registered: ignore (similar to epoll: no interest, no report).
        - If event_mask overlaps the registered interest mask:
            enqueue (fd, event_mask, data) onto the ready queue.

        Notes
        -----
        - This example does NOT deduplicate events. Calling trigger repeatedly can
          enqueue multiple entries for the same fd.
        - Real epoll has more nuanced behavior (edge vs level triggered, one-shot, etc.).
        """
        node = self._tree.search(fd)
        if node is None:
            # fd not registered; ignore (like real epoll)
            return

        # Only enqueue if the triggered events intersect the interest set.
        if event_mask & node.value["events"]:
            self._ready.append((fd, event_mask, node.value["data"]))

    def wait(self, timeout=None, maxevents=None):
        """
        Retrieve ready events from the ready queue, optionally waiting.

        Parameters
        ----------
        timeout : float | int | None
            - None  : wait indefinitely until at least one event is ready
            - 0     : do not block (poll)
            - > 0   : wait up to 'timeout' seconds

        maxevents : int | None
            - None  : return all currently queued ready events
            - int   : return at most this many events

        Returns
        -------
        list[tuple[int, int, any]]
            A list of (fd, event_mask, data) tuples.

        Behavior / Semantics
        --------------------
        - This uses a simple time-based loop and sleeps briefly to avoid a tight spin.
        - In real epoll_wait(), the kernel would block the thread efficiently until
          readiness is available, rather than sleeping/polling in user space.

        Complexity
        ----------
        - Waiting loop: depends on timeout and external triggers.
        - Draining events: O(k) where k is the number of returned events.
        """
        deadline = None
        if timeout is not None:
            deadline = time.monotonic() + timeout

        # Simple wait loop until something is ready or timeout expires.
        while not self._ready:
            if timeout == 0:
                break
            if deadline is not None and time.monotonic() >= deadline:
                break
            # In a real program, another thread or the OS would be filling _ready.
            time.sleep(0.001)

        events = []
        limit = maxevents if maxevents is not None else len(self._ready)
        while self._ready and len(events) < limit:
            events.append(self._ready.popleft())
        return events


# ---- Example event bitmasks (subset of real epoll flags) ----
EPOLLIN  = 0x001  # "readable"
EPOLLOUT = 0x004  # "writable"


if __name__ == "__main__":
    """
    Example usage / quick demo.

    We:
    1) Create EpollRB
    2) Register two fds with different interest masks
    3) Trigger readiness for both
    4) Call wait(timeout=0) to poll the ready queue without blocking
    """
    ep = EpollRB()

    # Register some "file descriptors"
    ep.register(10, EPOLLIN | EPOLLOUT, data="socket-10")
    ep.register(11, EPOLLIN,              data="socket-11")

    # Simulate: fd 10 becomes readable, fd 11 becomes writable
    ep.trigger(10, EPOLLIN)
    ep.trigger(11, EPOLLOUT)  # won't be queued; we only asked for EPOLLIN on fd 11

    # Non-blocking wait
    ready = ep.wait(timeout=0)
    for fd, ev, data in ready:
        print(f"fd={fd}, events={ev:#x}, data={data}")

    # Expected output:
    # fd=10, events=0x1, data=socket-10
