"""
kqueue.py
=============

A **toy** (learning-focused) kqueue implementation in pure Python.

What kqueue is (conceptually)
-----------------------------
`kqueue` is a BSD/macOS kernel event notification mechanism. You:

1) **Register** interest in certain events:
   - "fd X is readable"
   - "fd X is writable"
   - "timer fires every N ms"
   - (and many more: signals, process events, vnode/file changes, etc.)

2) **Wait** for events:
   - You call `kevent()` to apply changes and/or retrieve ready events.
   - The kernel blocks efficiently until something happens or a timeout expires.

This toy version mirrors the shape of the API:
- A `Kevent` object models the kernel's `struct kevent`.
- `Kqueue.kevent()` applies a "changelist" then returns up to `maxevents` ready events.
- `Kqueue.trigger()` simulates external events (in reality, the kernel would do this).
- `EVFILT_TIMER` is implemented via periodic timers checked by polling.

What this toy does NOT emulate
------------------------------
- True kernel-level blocking; we use a small `time.sleep()` loop.
- Edge-trigger semantics (EV_CLEAR) beyond a flag placeholder.
- Level-trigger semantics correctly (we enqueue once per trigger in this toy).
- Coalescing, deduplication, event “state”, backpressure, concurrency, races.
- Full fflags semantics, NOTE_* flags for vnode, signal delivery, etc.
- All kqueue filters; we only include READ/WRITE/TIMER.

Despite the simplifications, it teaches the important architecture:
**registrations** + **ready queue** + **kevent() = apply changes + retrieve readiness**.
"""

from collections import deque
import time

# ---------------------------------------------------------------------------
# Flags (subset) — these mirror names from BSD kqueue, but we only implement a few.
# ---------------------------------------------------------------------------

EV_ADD     = 0x0001   # add or modify a registration
EV_DELETE  = 0x0002   # remove a registration
EV_ENABLE  = 0x0004   # enable delivery for an existing registration
EV_DISABLE = 0x0008   # disable delivery for an existing registration
EV_ONESHOT = 0x0010   # automatically delete after delivering one event
EV_CLEAR   = 0x0020   # edge-trigger hint (not fully modeled here)

# ---------------------------------------------------------------------------
# Filters (subset) — in real kqueue, these are ints like EVFILT_READ=-1, etc.
# ---------------------------------------------------------------------------

EVFILT_READ  = -1     # fd is readable
EVFILT_WRITE = -2     # fd is writable
EVFILT_TIMER = -7     # periodic timer


class Kevent:
    """
    Python representation of BSD `struct kevent`.

    In BSD, `struct kevent` includes:
    - ident  : the identity of the event source (often an fd, but depends on filter)
    - filter : which type of event (READ, WRITE, TIMER, SIGNAL, ...)
    - flags  : EV_ADD/EV_DELETE/EV_ENABLE/EV_DISABLE/EV_ONESHOT/EV_CLEAR/...
    - fflags : filter-specific extra flags (NOTE_* for some filters)
    - data   : filter-specific value (e.g., bytes available, timer interval, etc.)
    - udata  : opaque user pointer returned back with the event

    In this toy:
    - `ident` is typically an integer (like an fd), but can be any hashable value.
    - `udata` is any Python object you want returned with the event.

    `__slots__` keeps instances lightweight (kqueue deals with many events).
    """
    __slots__ = ("ident", "filter", "flags", "fflags", "data", "udata")

    def __init__(self, ident, filter, flags=0, fflags=0, data=0, udata=None):
        self.ident = ident
        self.filter = filter
        self.flags = flags
        self.fflags = fflags
        self.data = data
        self.udata = udata

    def __repr__(self):
        """
        Developer-friendly representation, helpful for learning/debugging.
        """
        return (f"Kevent(ident={self.ident!r}, filter={self.filter}, "
                f"flags=0x{self.flags:x}, fflags=0x{self.fflags:x}, "
                f"data={self.data}, udata={self.udata!r})")


class Kqueue:
    """
    Toy kqueue implementation in pure Python.

    Core internal structures
    ------------------------
    1) Registrations table: `_registrations`
       Dict keyed by (ident, filter) containing a "registration record" with:
       - what we're watching (ident/filter)
       - how it should behave (enabled/oneshot/clear)
       - payload / metadata (fflags/data/udata)
       - timer state if filter == EVFILT_TIMER

    2) Ready queue: `_ready`
       A FIFO queue of `Kevent` objects to be returned by `kevent()`.

    How this maps to real kqueue
    ----------------------------
    Real kqueue has:
    - a kernel-managed registrations table
    - a kernel-managed queue of pending events

    Here:
    - `trigger()` manually injects an event for a given (ident, filter)
    - timers are polled in `_process_timers()`

    Semantics caveats
    -----------------
    - This toy is mostly "deliver on trigger". Real READ/WRITE filters are computed
      by kernel state (socket buffers, readiness, etc.).
    - EV_CLEAR is stored but not enforced as true edge-trigger semantics.
    """

    def __init__(self):
        """
        Initialize an empty Kqueue.

        `_registrations` entries have the shape:

            (ident, filter) -> {
                "ident": ident,
                "filter": filter,
                "flags": int,            # stored flags (not all meaningful)
                "fflags": int,           # filter-specific flags (mostly unused here)
                "data": int,             # filter-specific data
                "udata": any,            # user payload returned with events

                "enabled": bool,         # whether delivery is currently enabled
                "oneshot": bool,         # if True, remove after first delivery
                "clear": bool,           # EV_CLEAR hint (not fully modeled)

                # Timer-only fields:
                "timer_interval": float | None,  # seconds
                "next_fire": float | None,       # monotonic timestamp
            }

        `_ready` is a queue of `Kevent`s waiting to be returned.
        """
        self._registrations = {}
        self._ready = deque()

    # ---- internal helpers ----

    def _key(self, ident, filter):
        """
        Return the dictionary key used for registrations.

        Real kqueue uses (ident, filter) identity to distinguish registrations.
        For example:
        - fd=10 + EVFILT_READ
        - fd=10 + EVFILT_WRITE
        are distinct registrations.
        """
        return (ident, filter)

    def _apply_change(self, kev: Kevent):
        """
        Apply a single change request (one element of the `changelist`).

        In real kqueue, kevent() takes:
        - `changelist`: array of kevent structs describing add/mod/del/en/disable
        - `eventlist`:  array to fill with triggered events

        This method interprets `kev.flags` and mutates `_registrations` accordingly.

        Supported flag behavior:
        - EV_ADD:    create or update a registration
        - EV_DELETE: remove a registration
        - EV_ENABLE: enable event delivery for an existing registration
        - EV_DISABLE:disable event delivery for an existing registration

        Timer behavior (EVFILT_TIMER):
        - `kev.data` is interpreted as interval in milliseconds (kqueue convention)
        - when added, we compute next_fire = now + interval
        """
        key = self._key(kev.ident, kev.filter)
        flags = kev.flags

        # EV_ADD: create or update registration
        if flags & EV_ADD:
            reg = self._registrations.get(key)
            if reg is None:
                # Create a new registration record
                reg = {
                    "ident": kev.ident,
                    "filter": kev.filter,
                    "flags": 0,
                    "fflags": kev.fflags,
                    "data": kev.data,
                    "udata": kev.udata,

                    "enabled": True,
                    "oneshot": bool(flags & EV_ONESHOT),
                    "clear": bool(flags & EV_CLEAR),

                    "timer_interval": None,
                    "next_fire": None,
                }
                self._registrations[key] = reg

            # Update registration fields (treat EV_ADD as "add or modify")
            reg["flags"] |= flags
            reg["fflags"] = kev.fflags
            reg["data"] = kev.data
            reg["udata"] = kev.udata
            reg["enabled"] = not bool(flags & EV_DISABLE)
            reg["oneshot"] = bool(flags & EV_ONESHOT)
            reg["clear"] = bool(flags & EV_CLEAR)

            # Timer setup (filter-specific semantics)
            if kev.filter == EVFILT_TIMER:
                # Like real kqueue: data is interval in milliseconds
                interval_sec = kev.data / 1000.0
                reg["timer_interval"] = interval_sec
                reg["next_fire"] = time.monotonic() + interval_sec

        # EV_DELETE: remove registration completely
        if flags & EV_DELETE:
            self._registrations.pop(key, None)
            return

        # EV_ENABLE: enable an existing registration
        if flags & EV_ENABLE:
            reg = self._registrations.get(key)
            if reg is not None:
                reg["enabled"] = True

                # If enabling a timer that isn't scheduled, schedule its next_fire
                if reg["filter"] == EVFILT_TIMER and reg["next_fire"] is None:
                    interval = reg["timer_interval"]
                    if interval is not None:
                        reg["next_fire"] = time.monotonic() + interval

        # EV_DISABLE: disable an existing registration
        if flags & EV_DISABLE:
            reg = self._registrations.get(key)
            if reg is not None:
                reg["enabled"] = False

    def _enqueue_event(self, reg, triggered_data=None):
        """
        Convert a registration record into a delivered Kevent and append it to `_ready`.

        Parameters
        ----------
        reg : dict
            A registration record from `_registrations`.
        triggered_data : any, optional
            If provided, overrides the `data` field in the delivered event.
            This is useful for simulated events where you want to attach a
            measured quantity (e.g., "123 bytes available").

        Side effects
        ------------
        - Appends a new `Kevent` to `_ready`.
        - If registration is EV_ONESHOT, removes it after enqueuing.
        """
        kev = Kevent(
            ident=reg["ident"],
            filter=reg["filter"],
            flags=reg["flags"],
            fflags=reg["fflags"],
            data=triggered_data if triggered_data is not None else reg["data"],
            udata=reg["udata"],
        )
        self._ready.append(kev)

        # EV_ONESHOT: remove after first delivery
        if reg["oneshot"]:
            self._registrations.pop(self._key(reg["ident"], reg["filter"]), None)

    def _process_timers(self):
        """
        Scan timer registrations and enqueue any that have expired.

        Real kqueue timers are maintained by the kernel and fire without polling.
        Here, we emulate timer firing by checking all timer regs each time we
        are waiting for events.

        Behavior
        --------
        For each enabled timer registration:
        - if now >= next_fire:
            enqueue one event
            reschedule next_fire = now + interval (unless it was oneshot)
        """
        now = time.monotonic()

        # Iterate over a snapshot so we can modify the dict while iterating.
        for key, reg in list(self._registrations.items()):
            if reg["filter"] == EVFILT_TIMER and reg["enabled"]:
                interval = reg["timer_interval"]
                next_fire = reg["next_fire"]
                if interval is not None and next_fire is not None and now >= next_fire:
                    self._enqueue_event(reg)

                    # If still registered & not oneshot, reschedule
                    if self._registrations.get(key) is reg and reg["timer_interval"] is not None:
                        reg["next_fire"] = now + interval

    # ---- public interface ----

    def kevent(self, changelist=None, maxevents=0, timeout=None):
        """
        Apply registration changes, then retrieve ready events (optionally waiting).

        This mirrors the signature shape of BSD `kevent()`:

            kevent(kq, changelist, nchanges, eventlist, nevents, timeout)

        In this toy:
        - `changelist` is an iterable of Kevent objects describing modifications.
        - returned value is a Python list of delivered Kevent objects.

        Parameters
        ----------
        changelist : iterable[Kevent] | None
            The set of registration changes to apply before waiting.
            Common uses:
            - Add a read watch for fd=10
            - Delete a watch
            - Enable/disable a watch
            - Add a timer
        maxevents : int | None
            Controls event retrieval:
            - 0: apply changelist only; do not wait; return []
            - >0: return up to this many events
            - None or <=0: treat as "return everything currently ready"
        timeout : float | int | None
            Waiting behavior:
            - None: block (in this toy: poll+sleep) until at least one event is ready
            - 0: non-blocking poll (return immediately with what's ready)
            - >0: wait up to `timeout` seconds

        Returns
        -------
        list[Kevent]
            Up to `maxevents` events pulled from the ready queue.

        Notes
        -----
        - In real kqueue, EV_CLEAR affects whether an event remains “active” until drained.
          We do not model that state machine; we enqueue when triggered and that's it.
        - This loop uses a tiny sleep to avoid a tight spin; in the kernel, waiting is efficient.
        """
        # 1) Apply changes
        if changelist:
            for kev in changelist:
                self._apply_change(kev)

        # If caller only wanted to apply changes, return immediately
        if maxevents == 0:
            return []

        # 2) Wait for events (poll timers + optional sleep)
        deadline = None
        if timeout is not None:
            deadline = time.monotonic() + timeout

        while not self._ready:
            # Timers may generate events
            self._process_timers()
            if self._ready:
                break

            # Timeout logic
            if timeout == 0:
                break
            if deadline is not None and time.monotonic() >= deadline:
                break

            # In real kqueue, the kernel blocks; here we busy-sleep lightly
            time.sleep(0.001)

        # 3) Collect up to maxevents events
        if maxevents is None or maxevents <= 0:
            maxevents = len(self._ready)

        events = []
        while self._ready and len(events) < maxevents:
            events.append(self._ready.popleft())
        return events

    def trigger(self, ident, filter, data=None):
        """
        Simulate an external event matching (ident, filter).

        Example mental mapping:
        - (fd=10, EVFILT_READ): "socket fd 10 is readable now"
        - (fd=10, EVFILT_WRITE): "socket fd 10 is writable now"

        Parameters
        ----------
        ident : hashable
            Identity of the event source; typically an integer “fd” in examples.
        filter : int
            One of EVFILT_READ / EVFILT_WRITE / EVFILT_TIMER (though timers
            are typically driven internally via _process_timers()).
        data : any, optional
            Value to attach to the delivered event's `data` field, overriding
            the stored registration data.

        Behavior
        --------
        - If there is no matching registration, or it is disabled: do nothing.
        - Otherwise, enqueue a delivered Kevent into `_ready`.
        - If the registration was EV_ONESHOT, it is removed after first enqueue.

        Note
        ----
        Real kqueue does not have a user-called trigger; the kernel populates events.
        This exists purely to make the model interactive and testable.
        """
        key = self._key(ident, filter)
        reg = self._registrations.get(key)
        if not reg or not reg["enabled"]:
            return
        self._enqueue_event(reg, triggered_data=data)


if __name__ == "__main__":
    """
    Quick demo:
    - Register a READ watch for ident=10 (pretend it's fd 10).
    - Register a periodic timer firing every 500ms.
    - Trigger a READ event manually (simulating kernel readiness).
    - Call kevent(timeout=0) to poll immediately.
    - Call kevent(timeout=1.0) to wait and observe at least one timer tick.
    """
    kq = Kqueue()

    # Register: "fd 10 is interesting for READ"
    kq.kevent([
        Kevent(
            ident=10,
            filter=EVFILT_READ,
            flags=EV_ADD,
            data=0,
            udata="socket-10"
        )
    ])

    # Register: timer that fires every 500 ms (data is in ms)
    kq.kevent([
        Kevent(
            ident=1,
            filter=EVFILT_TIMER,
            flags=EV_ADD,
            data=500,            # 500 ms
            udata="timer-500ms"
        )
    ])

    # Somewhere else: we "notice" fd 10 is readable
    # (in real life: kernel does this; here we simulate)
    kq.trigger(10, EVFILT_READ, data=123)

    # Non-blocking poll (timeout=0)
    ready_now = kq.kevent([], maxevents=10, timeout=0)
    print("ready (non-blocking):")
    for ev in ready_now:
        print(" ", ev)

    # Wait up to 1 second to see the timer fire
    ready_timer = kq.kevent([], maxevents=10, timeout=1.0)
    print("ready (after waiting for timer):")
    for ev in ready_timer:
        print(" ", ev)
