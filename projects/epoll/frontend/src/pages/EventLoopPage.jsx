import React from "react";
import Section from "../components/layout/Section";
import CodeBlock from "../components/common/CodeBlock";
import ConceptCard from "../components/common/ConceptCard";

import eventLoopCode from "../../algorithms/event-loop/event_loop.py?raw";

const eventLoopRun = () => `
from event_loop import EventLoop, Sleep

def tracer(name):
    print(f"{name}: start")
    yield Sleep(0.001)
    print(f"{name}: woke up after sleep")
    yield Sleep(0.001)
    print(f"{name}: done")

loop = EventLoop()
loop.create_task(tracer("task-a"))
loop.create_task(tracer("task-b"))
loop.run_forever()
`;

function EventLoopPage() {
  return (
    <div className="page">
      <Section eyebrow="Step 3" title="Event loops: putting it all together">
        <p>
          <strong>epoll</strong> (Linux) and <strong>kqueue</strong> (BSD/macOS)
          are low-level OS primitives for one specific job:
          <strong> efficiently waiting for many I/O sources at once</strong>.
        </p>

        <p>
          But those primitives don’t schedule your application logic. They don’t
          know what a “request handler”, “timer”, or “retry later” means. That’s
          the job of an <strong>event loop</strong>: a user-space orchestrator
          that repeatedly:
        </p>

        <ul>
          <li>
            runs a bit of work for each <strong>task</strong> (a coroutine /
            generator),
          </li>
          <li>
            pauses tasks when they would otherwise block (sleep, read, write),
          </li>
          <li>
            and resumes tasks when the OS says their condition is ready.
          </li>
        </ul>

        <p>
          This learning module builds a minimal “async runtime” similar in spirit
          to <code>asyncio</code>, <code>trio</code>, and the Node.js event loop:
          you’ll see the core mechanisms without the production-level complexity.
        </p>
      </Section>

      <Section title="The key idea: coroutines yield “what I’m waiting for”">
        <div className="cards-grid">
          <ConceptCard title="Cooperative scheduling: tasks run until they yield">
            <p>
              In a thread-based model, the OS preempts you: it can interrupt a
              running thread at almost any time. In an event loop, scheduling is{" "}
              <strong>cooperative</strong>:
            </p>
            <ul>
              <li>A task runs until it reaches a point where it can’t proceed.</li>
              <li>
                Instead of blocking the whole program, it <code>yield</code>s an
                “operation” describing what it needs.
              </li>
              <li>The event loop parks the task and runs something else.</li>
            </ul>
            <p>
              That’s why the yielded objects (<code>Sleep</code>,{" "}
              <code>ReadWait</code>, <code>WriteWait</code>) are so important:
              they are the task’s way of talking to the scheduler.
            </p>
          </ConceptCard>

          <ConceptCard title="Yielded primitives: Sleep / ReadWait / WriteWait">
            <p>
              Instead of using Python’s <code>await</code> syntax (which requires
              a full Future/Task framework), this loop uses generator coroutines
              that yield small “intent” objects:
            </p>
            <ul>
              <li>
                <code>Sleep(delay)</code> → “wake me up in{" "}
                <code>delay</code> seconds”
              </li>
              <li>
                <code>ReadWait(fileobj)</code> → “resume me when this file/socket
                becomes readable”
              </li>
              <li>
                <code>WriteWait(fileobj)</code> → “resume me when this becomes
                writable”
              </li>
            </ul>
            <p>
              Conceptually, these correspond to things like{" "}
              <code>await asyncio.sleep(...)</code>,{" "}
              <code>await loop.sock_recv(...)</code>, and{" "}
              <code>await loop.sock_sendall(...)</code>.
            </p>
          </ConceptCard>

          <ConceptCard title="Why “writable” matters (non-blocking connect)">
            <p>
              A subtle but crucial detail: sockets becoming <strong>writable</strong>{" "}
              is used for more than “I can send data.” In non-blocking networking,
              a socket often becomes writable when a <code>connect()</code>{" "}
              finishes.
            </p>
            <p>
              That’s why your <code>client_task()</code> yields{" "}
              <code>WriteWait(sock)</code> right after initiating the connection:
              it’s waiting for the OS to say “connect completed.”
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Your event loop architecture (data structures)">
        <div className="cards-grid">
          <ConceptCard title="_ready: the runnable queue (who can run now?)">
            <p>
              <code>_ready</code> is a FIFO queue of tasks that are ready to take
              their next step immediately. When a task is in <code>_ready</code>,
              the loop will soon call <code>next(task.coro)</code>.
            </p>
            <p>
              Key idea: tasks are run in small increments (one yield at a time),
              which is what makes a single-threaded program feel concurrent.
            </p>
          </ConceptCard>

          <ConceptCard title="_sleeping: timers with a min-heap (who wakes next?)">
            <p>
              <code>Sleep(delay)</code> doesn’t block the process. The loop
              computes a wake-up time and stores the task in{" "}
              <code>_sleeping</code>, a heap ordered by the earliest deadline.
            </p>
            <p>
              Using a heap makes “find the next timer to expire” efficient:
              <code>_sleeping[0]</code> is always the soonest wake-up.
            </p>
          </ConceptCard>

          <ConceptCard title="_selector: OS-backed I/O readiness (who is readable/writable?)">
            <p>
              The <code>selectors.DefaultSelector</code> is the portability layer
              that uses <strong>epoll</strong>, <strong>kqueue</strong>, or
              similar mechanisms under the hood depending on your OS.
            </p>
            <p>
              Your loop registers file objects along with:
            </p>
            <ul>
              <li>a mask: READ or WRITE</li>
              <li>the waiting Task (stored as selector “data”)</li>
            </ul>
            <p>
              When <code>select()</code> returns readiness events, the loop turns
              them back into runnable tasks by moving them into <code>_ready</code>.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="The core loop: what run_forever() is actually doing">
        <div className="cards-grid">
          <ConceptCard title="1) Wake timers first">
            <p>
              Each iteration begins by checking whether any sleeping tasks have
              reached their deadline. Expired tasks get moved from{" "}
              <code>_sleeping</code> to <code>_ready</code>.
            </p>
            <p>
              This ensures timers fire promptly even if there’s no I/O happening.
            </p>
          </ConceptCard>

          <ConceptCard title="2) If nothing is runnable, block efficiently">
            <p>
              If <code>_ready</code> is empty, the loop calculates a timeout:
            </p>
            <ul>
              <li>
                if there’s a sleeping task, timeout = time until the next wakeup
              </li>
              <li>otherwise, timeout can be infinite (wait for I/O)</li>
            </ul>
            <p>
              Then it calls <code>selector.select(timeout)</code>. This is the
              crucial step that makes the loop efficient: you’re not busy-waiting
              or scanning everything—you're letting the OS wake you up.
            </p>
          </ConceptCard>

          <ConceptCard title="3) Run each ready task once (fairness)">
            <p>
              The loop snapshots <code>n_ready</code> and advances exactly that
              many tasks by one step. That detail matters:
            </p>
            <ul>
              <li>
                It prevents one task from repeatedly re-queuing itself and
                starving others in the same iteration.
              </li>
              <li>
                It creates a simple round-robin rhythm: each runnable task gets a
                turn.
              </li>
            </ul>
            <p>
              In production loops, fairness can get much more sophisticated, but
              this pattern is a great learning baseline.
            </p>
          </ConceptCard>

          <ConceptCard title="4) Interpret the yielded operation and reschedule">
            <p>
              Each <code>next()</code> call returns an “operation” object. The
              loop uses <code>isinstance</code> checks to decide where the task
              goes next:
            </p>
            <ul>
              <li>
                <code>Sleep</code> → push into <code>_sleeping</code> heap
              </li>
              <li>
                <code>ReadWait</code>/<code>WriteWait</code> → register with{" "}
                <code>_selector</code>
              </li>
              <li>
                unknown yield → treat as “yield control” and put back in{" "}
                <code>_ready</code>
              </li>
            </ul>
            <p>
              This is the heart of a scheduler: move tasks between “ready” and
              “waiting” sets based on what they need.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Echo server demo: event-driven networking without threads">
        <p>
          The bottom half of <code>event_loop.py</code> is a complete mini demo:
          an echo server and a client running on the same custom loop.
        </p>

        <div className="cards-grid">
          <ConceptCard title="echo_server(): accept loop as a coroutine">
            <p>
              <code>echo_server(sock, loop)</code> waits for the listening socket
              to become readable. “Readable” on a listening socket means: there’s
              at least one pending connection to accept.
            </p>
            <p>
              Once accepted, it spawns a per-connection handler via{" "}
              <code>loop.create_task(handle_client(...))</code>. That’s how you
              get concurrency: each client is its own task.
            </p>
          </ConceptCard>

          <ConceptCard title="handle_client(): alternating read and write readiness">
            <p>
              <code>handle_client(conn)</code> cycles:
            </p>
            <ul>
              <li>
                yield <code>ReadWait(conn)</code> → wait for inbound bytes
              </li>
              <li>
                recv data → if empty, client closed
              </li>
              <li>
                yield <code>WriteWait(conn)</code> → wait until we can send
              </li>
              <li>
                send data back (echo)
              </li>
            </ul>
            <p>
              That “read → process → write” loop is the backbone of many network
              protocols.
            </p>
          </ConceptCard>

          <ConceptCard title="client_task(): non-blocking connect and teardown">
            <p>
              The client uses a non-blocking socket. It initiates{" "}
              <code>connect()</code> (which likely raises{" "}
              <code>BlockingIOError</code>), then yields{" "}
              <code>WriteWait(sock)</code> to wait for connection completion.
            </p>
            <p>
              After receiving the echo, it calls <code>loop.stop()</code> so the
              script exits cleanly.
            </p>
          </ConceptCard>
        </div>

        <p>
          If you replaced <code>selectors</code> with a direct <code>epoll</code>{" "}
          backend (or extended this with proper Futures, cancellation, and
          exception handling), you’d be building the skeleton of a real async
          runtime.
        </p>

        <CodeBlock
          title="EventLoop, tasks, and echo server"
          filename="algorithms/event-loop/event_loop.py"
          code={eventLoopCode}
          runSnippet={eventLoopRun}
        />
      </Section>

      <Section title="Connecting all three layers">
        <p>
          Big-picture stack from bottom to top (what you’ve built across the
          module):
        </p>
        <ol>
          <li>
            <strong>Kernel data structures</strong> (epoll readiness engine):
            RB-tree interest set + ready list so the kernel can manage huge
            numbers of watched fds efficiently.
          </li>
          <li>
            <strong>General event multiplexer</strong> (kqueue / epoll concept):
            unify many event sources behind one “wait for events” primitive.
          </li>
          <li>
            <strong>User-space event loop</strong>: schedule your coroutines,
            manage timers, interpret readiness into progress on higher-level work.
          </li>
        </ol>
        <p>
          This is why event loops are such a powerful abstraction: the OS gives
          you readiness signals, and the loop turns those signals into structured
          concurrency.
        </p>
      </Section>
    </div>
  );
}

export default EventLoopPage;
