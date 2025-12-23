import React from "react";
import Section from "../components/layout/Section";
import CodeBlock from "../components/common/CodeBlock";
import ConceptCard from "../components/common/ConceptCard";

import kqueueCode from "../../algorithms/kqueue/kqueue.py?raw";

const kqueueRun = ({ sessionDir, mainFile }) => `
import runpy
runpy.run_path("${sessionDir}/${mainFile}", run_name="__main__")
`;

function KqueuePage() {
  return (
    <div className="page">
      <Section
        eyebrow="Step 2"
        title="kqueue: a more general event notification system"
      >
        <p>
          <strong>epoll</strong> (Linux) and <strong>kqueue</strong> (BSD/macOS)
          solve the same core problem: <strong>wait efficiently for many events</strong>{" "}
          without scanning everything in a loop.
        </p>

        <p>
          The difference is scope. <strong>epoll</strong> is primarily about file
          descriptors (readable/writable). <strong>kqueue</strong> is designed as a{" "}
          <em>general event notification bus</em>: it can deliver readiness events
          for I/O, timers, signals, process state changes, filesystem events, and more.
        </p>

        <ul>
          <li>Readable / writable sockets and files</li>
          <li>Timers (periodic or one-shot)</li>
          <li>Signals (e.g. SIGINT)</li>
          <li>Process exit and other process events</li>
          <li>Filesystem/vnode changes (platform dependent)</li>
        </ul>

        <p>
          Another important design difference: kqueue uses a single syscall-shaped
          interface—<code>kevent()</code>—for both{" "}
          <strong>configuration</strong> (add/modify/delete watches) and{" "}
          <strong>event retrieval</strong> (return the ready events). You submit
          “changes” and receive “events” using the same struct.
        </p>
      </Section>

      <Section title="Two-phase mental model: register, then wait">
        <div className="cards-grid">
          <ConceptCard title="Phase 1: register interest (changelist)">
            <p>
              You first describe what you care about by submitting a{" "}
              <strong>changelist</strong>: “watch ident X with filter Y using these
              flags and settings.”
            </p>
            <p>
              In the real API, this is still done through <code>kevent()</code>.
              Your toy model reflects that by having <code>kevent(changelist, ...)</code>{" "}
              apply changes before it waits/returns results.
            </p>
          </ConceptCard>

          <ConceptCard title="Phase 2: retrieve readiness (eventlist)">
            <p>
              After registering interest, you repeatedly ask: “what’s ready now?”
              The kernel returns only the events that are actually ready.
            </p>
            <p>
              That’s the scalability win: the application processes{" "}
              <code>O(#ready)</code> events, not <code>O(#watched)</code> watches.
            </p>
          </ConceptCard>

          <ConceptCard title="Why this abstraction is powerful">
            <p>
              Because timers, signals, and I/O all flow through the same mechanism,
              a user-space event loop can treat them uniformly:
              <strong> register → wait → dispatch</strong>.
            </p>
            <p>
              That’s why kqueue makes a good foundation for high-level runtimes:
              it unifies many sources of “wake me up when…” behind one API.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Kevent & Kqueue in your model">
        <div className="cards-grid">
          <ConceptCard title="Kevent: the core message (both change and event)">
            <p>
              Your <code>Kevent</code> class is the heart of the design because it
              plays <strong>two roles</strong>:
            </p>
            <ul>
              <li>
                As a <strong>change request</strong> (add/delete/enable/disable a watch)
              </li>
              <li>
                As a <strong>delivered event</strong> (something happened; here’s ident/filter/data)
              </li>
            </ul>

            <p>
              The key fields mirror the C <code>struct kevent</code> idea:
            </p>
            <ul>
              <li>
                <code>ident</code> — the thing being watched (fd, timer id, pid, etc.)
              </li>
              <li>
                <code>filter</code> — the category/type:{" "}
                <code>EVFILT_READ</code>, <code>EVFILT_WRITE</code>,{" "}
                <code>EVFILT_TIMER</code>, …
              </li>
              <li>
                <code>flags</code> — how the watch behaves and what operation to apply:
                <code>EV_ADD</code>, <code>EV_DELETE</code>,{" "}
                <code>EV_ENABLE</code>, <code>EV_DISABLE</code>,{" "}
                <code>EV_ONESHOT</code>, <code>EV_CLEAR</code>
              </li>
              <li>
                <code>data</code> — filter-specific numeric data:
                in your timer model, it’s the interval in milliseconds
              </li>
              <li>
                <code>udata</code> — arbitrary user payload returned with the event
              </li>
            </ul>

            <p>
              Learning lens: think of <code>Kevent</code> as the “packet format”
              for the kqueue bus—everything flows through it.
            </p>
          </ConceptCard>

          <ConceptCard title="Kqueue: registrations table + ready queue">
            <p>
              Your <code>Kqueue</code> maintains two important internal structures:
            </p>

            <ul>
              <li>
                A <strong>registration table</strong> (dictionary) mapping{" "}
                <code>(ident, filter) → registration</code>. This is the set of
                everything you’re currently watching.
              </li>
              <li>
                A <strong>ready queue</strong> (<code>deque</code>) containing
                <code>Kevent</code> objects waiting to be returned to the caller.
              </li>
            </ul>

            <p>
              The big idea: registrations describe <em>potential</em> events; the
              ready queue contains <em>actual</em> events that occurred.
            </p>

            <p>
              Your <code>kevent(changelist, maxevents, timeout)</code> method
              reflects real kqueue usage:
            </p>
            <ol>
              <li>Apply each change in the changelist (ADD/DEL/ENABLE/DISABLE).</li>
              <li>Optionally wait for something to become ready.</li>
              <li>Return up to <code>maxevents</code> ready events.</li>
            </ol>
          </ConceptCard>

          <ConceptCard title="Timer filter: EVFILT_TIMER as a first-class event source">
            <p>
              A key difference from epoll-style thinking is that timers are not
              “bolted on” in a separate API—they’re modeled as just another filter.
            </p>

            <p>
              In your code, a timer registration stores:
            </p>
            <ul>
              <li>
                an interval (derived from <code>data</code> milliseconds),
              </li>
              <li>
                and a <code>next_fire</code> timestamp computed using{" "}
                <code>time.monotonic()</code>.
              </li>
            </ul>

            <p>
              Then <code>_process_timers()</code> checks for expirations, enqueues
              a timer <code>Kevent</code>, and reschedules it (unless oneshot).
            </p>

            <p>
              This demonstrates the “unified multiplexer” point: timers and I/O
              are treated the same way at the API boundary.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Semantics notes (important for learning)">
        <div className="cards-grid">
          <ConceptCard title="EV_ONESHOT: deliver once, then remove">
            <p>
              With <code>EV_ONESHOT</code>, the registration self-destructs after
              the first delivered event. Your implementation models this directly:
              once an event is enqueued, the registration is removed.
            </p>
            <p>
              This is useful for patterns like “wake me up once when this becomes ready”
              and can reduce duplicate notifications in some designs.
            </p>
          </ConceptCard>

          <ConceptCard title="EV_CLEAR: edge-trigger hint (not fully emulated)">
            <p>
              Real <code>EV_CLEAR</code> semantics are subtle: they relate to whether
              you get repeated events while a condition stays true (level-triggered)
              versus only when it transitions (edge-triggered).
            </p>
            <p>
              In this toy, <code>EV_CLEAR</code> is tracked as a flag but not used to
              implement the full edge-trigger state machine. That’s fine for learning
              the architecture, but it’s a good reminder that production multiplexers
              have nuanced semantics.
            </p>
          </ConceptCard>

          <ConceptCard title="trigger(): a teaching hook">
            <p>
              The real kernel produces readiness events automatically; user code
              never calls “trigger.” Your <code>.trigger()</code> exists so you can
              simulate what the kernel would do and see how events flow into the
              ready queue and out through <code>kevent()</code>.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Walking through the demo">
        <p>
          The <code>__main__</code> block demonstrates the typical usage pattern:
        </p>

        <ol>
          <li>
            Register <code>ident=10</code> with <code>EVFILT_READ</code> to watch a
            pretend “socket”.
          </li>
          <li>
            Register <code>ident=1</code> with <code>EVFILT_TIMER</code> for a 500ms
            periodic timer (stored in <code>data</code> as milliseconds).
          </li>
          <li>
            Simulate readiness: call <code>.trigger(10, EVFILT_READ, data=123)</code>.
            That <code>data</code> value becomes the delivered event’s <code>data</code>.
          </li>
          <li>
            Poll immediately with <code>timeout=0</code> to retrieve what’s already ready.
          </li>
          <li>
            Then wait up to 1 second; the timer will fire and you’ll see a timer event.
          </li>
        </ol>

        <p>
          A helpful way to read the code is to trace the life of a single event:
          registration → trigger/timer expiry → enqueue → returned by <code>kevent()</code>.
        </p>

        <CodeBlock
          title="Kqueue & Kevent: generalized event notification"
          filename="algorithms/kqueue/kqueue.py"
          code={kqueueCode}
          runSnippet={kqueueRun}
        />
      </Section>

      <Section title="Where this sits in the stack">
        <p>
          In the overall learning sequence:
        </p>
        <ol>
          <li>
            <strong>epoll</strong> taught the core data structures: interest set + ready list.
          </li>
          <li>
            <strong>kqueue</strong> generalizes the idea into a unified event bus:
            I/O + timers (and many more) through one interface.
          </li>
          <li>
            Next, an <strong>event loop</strong> uses these primitives to schedule coroutines
            and build higher-level servers and protocols.
          </li>
        </ol>
      </Section>
    </div>
  );
}

export default KqueuePage;
