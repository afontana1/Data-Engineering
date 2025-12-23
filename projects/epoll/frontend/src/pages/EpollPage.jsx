import React from "react";
import Section from "../components/layout/Section";
import CodeBlock from "../components/common/CodeBlock";
import ConceptCard from "../components/common/ConceptCard";

import epollRbCode from "../../algorithms/epoll-rbtree/epoll_rbtree.py?raw";
import rbTreeCode from "../../algorithms/epoll-rbtree/rbtree.py?raw";

const rbTreeRun = () => `
from rbtree import RBTree

tree = RBTree()
for key in [10, 2, 7, 15, 1]:
    tree.insert(key, f"value-{key}")

print("inorder after inserts:", tree.inorder())
tree.delete(7)
print("inorder after deleting 7:", tree.inorder())
`;

const epollRun = ({ sessionDir }) => `
import runpy
runpy.run_path("${sessionDir}/epoll_rbtree.py", run_name="__main__")
`;

function EpollPage() {
  return (
    <div className="page">
      <Section
        eyebrow="Step 1"
        title="epoll + Red-Black Tree: a scalable readiness engine"
      >
        <p>
          Imagine a server that needs to watch thousands (or hundreds of
          thousands) of sockets. The core question is:
          <strong> “Which sockets can I read from or write to right now?”</strong>
        </p>

        <p>
          Older APIs like <code>select()</code> and <code>poll()</code> answer
          that question by forcing you to scan <em>every</em> file descriptor on
          every tick. If you watch <code>n</code> descriptors, that scan costs{" "}
          <code>O(n)</code> per loop iteration—wasteful when only a small subset
          is actually ready.
        </p>

        <p>
          <strong>epoll</strong> flips the model. Instead of repeatedly scanning
          a big list, it maintains two kernel-managed structures:
        </p>

        <ul>
          <li>
            An <strong>interest set</strong>: “what I care about” (watched file
            descriptors + which events). This needs fast add/remove/lookup.
          </li>
          <li>
            A <strong>ready list</strong>: “what happened” (only the descriptors
            that became ready). This needs fast retrieval by{" "}
            <code>epoll_wait()</code>.
          </li>
        </ul>

        <p>
          The key optimization: if only <code>k</code> descriptors are ready,
          then retrieving readiness should be closer to <code>O(k)</code>, not{" "}
          <code>O(n)</code>.
        </p>
      </Section>

      <Section title="Mental model: what epoll is optimizing">
        <div className="cards-grid">
          <ConceptCard title="Two-phase design: register once, wait many times">
            <p>
              epoll splits the work into two phases:
            </p>
            <ol>
              <li>
                <strong>Registration/configuration</strong>: you tell the kernel
                what to watch (add/modify/delete). This can be{" "}
                <code>O(log n)</code> because it’s not on the hot path every
                tick.
              </li>
              <li>
                <strong>Event retrieval</strong>: you block waiting for readiness
                and get back only the ready descriptors. This should be fast and
                scale with <code>#ready</code>.
              </li>
            </ol>
            <p>
              The module mirrors that separation with an RB-tree for
              registrations and a queue for ready events.
            </p>
          </ConceptCard>

          <ConceptCard title="Why a tree and a queue?">
            <p>
              These two structures solve different problems:
            </p>
            <ul>
              <li>
                <strong>Interest set</strong> needs:
                <ul>
                  <li>fast lookup by fd (is it registered?)</li>
                  <li>fast insert/delete (clients connect/disconnect)</li>
                  <li>stable performance as it grows</li>
                </ul>
              </li>
              <li>
                <strong>Ready list</strong> needs:
                <ul>
                  <li>fast append when readiness occurs</li>
                  <li>fast pop when the app calls wait</li>
                  <li>preserve order of arrival (often useful)</li>
                </ul>
              </li>
            </ul>
            <p>
              In the toy implementation: RB-tree = interest set, deque = ready
              list.
            </p>
          </ConceptCard>

          <ConceptCard title="What this toy does and does NOT model">
            <p>
              This is a learning model, not a kernel reimplementation.
              It captures the core architecture (interest set + ready list) but
              intentionally skips many real-world details:
            </p>
            <ul>
              <li>
                ✅ models: add/mod/del, “readiness occurs”, wait returns events
              </li>
              <li>
                ❌ not modeled: edge-triggered vs level-triggered semantics,
                EPOLLONESHOT, wakeup mechanisms, concurrency, fd lifecycle races,
                internal kernel locking, and interactions with real drivers
              </li>
            </ul>
            <p>
              That’s a good thing for learning—fewer moving parts, clearer focus
              on the key ideas.
            </p>
          </ConceptCard>
        </div>
      </Section>

      <Section title="How The EpollRB model maps to the real thing">
        <div className="cards-grid">
          <ConceptCard title="Interest set in an RB-tree">
            <p>
              In the Linux kernel, each epoll instance maintains an internal set
              of watched descriptors. That set must support:
              <strong> insert, delete, and lookup by fd</strong> efficiently.
            </p>

            <p>
              Historically (and conceptually), a balanced tree is a natural fit:
              it guarantees <code>O(log n)</code> operations by keeping the
              height of the structure bounded even in adversarial insertion
              orders.
            </p>

            <p>
              In The toy:
              <br />
              <code>fd → {"{ events: event_mask, data: user_data }"}</code>
            </p>

            <p>
              Every “control operation” becomes a tree operation:
            </p>
            <ul>
              <li>
                <strong>ADD</strong> → insert into the tree (<code>O(log n)</code>)
              </li>
              <li>
                <strong>MOD</strong> → search + update (<code>O(log n)</code>)
              </li>
              <li>
                <strong>DEL</strong> → delete from the tree (<code>O(log n)</code>)
              </li>
            </ul>

            <p>
              The <code>RBTree</code> in <code>rbtree.py</code> models this with:
              rotations (structural changes) + recoloring (constraint repair) to
              maintain balance.
            </p>
          </ConceptCard>

          <ConceptCard title="Ready queue">
            <p>
              The epoll “magic” is that the kernel doesn’t need to scan
              everything when something becomes ready. Instead:
              <strong> the I/O subsystem notifies epoll</strong>, and epoll
              appends a record into a ready list.
            </p>

            <p>
              In The toy, the ready list is a <code>deque</code> stored in{" "}
              <code>_ready</code>. The <code>.trigger()</code> method plays the
              role of “the kernel just detected readiness”.
            </p>

            <p>
              Important detail: <code>trigger()</code> doesn’t blindly enqueue.
              It checks whether the readiness event intersects the interest mask:
            </p>
            <ul>
              <li>
                registered interest: <code>events</code>
              </li>
              <li>
                observed readiness: <code>event_mask</code>
              </li>
              <li>
                enqueue only if: <code>event_mask &amp; events</code> is non-zero
              </li>
            </ul>

            <p>
              This “mask overlap” is the core contract of epoll-style APIs.
            </p>
          </ConceptCard>

          <ConceptCard title="Waiter: epoll_wait()">
            <p>
              <code>epoll_wait()</code> conceptually does one job:
              block until the ready list is non-empty, then return ready items.
            </p>

            <p>
              That’s why the retrieval cost is closer to{" "}
              <code>O(#ready)</code> rather than <code>O(#watched)</code>.
            </p>

            <p>
              In The implementation, <code>.wait(timeout, maxevents)</code>{" "}
              approximates that behavior:
            </p>

            <ul>
              <li>
                <code>timeout=None</code> → “wait forever” (in real epoll, the
                kernel blocks efficiently; here we loop + sleep)
              </li>
              <li>
                <code>timeout=0</code> → non-blocking poll (return immediately)
              </li>
              <li>
                <code>timeout&gt;0</code> → stop waiting once the deadline passes
              </li>
              <li>
                <code>maxevents</code> → cap how many you pull from the ready list
              </li>
            </ul>
          </ConceptCard>
        </div>
      </Section>

      <Section title="Data structures: RBNode & RBTree">
        <p>
          The red-black tree is the workhorse data structure behind the interest
          set. The point of the RB constraints is simple:
          <strong> keep the tree height bounded</strong>, which keeps all core
          operations fast.
        </p>

        <p>
          The practical consequence: even if you insert keys in “bad” order (like
          increasing fds), you don’t get a degenerate linked list. The structure
          self-corrects via rotations and recoloring so the height remains{" "}
          <code>O(log n)</code>.
        </p>

        <p>Key operations to look for in the code:</p>
        <ul>
          <li>
            <code>insert()</code>: standard BST insert + RB repair via{" "}
            <code>_insert_fixup()</code>
          </li>
          <li>
            <code>delete()</code>: BST deletion cases + RB repair via{" "}
            <code>_delete_fixup()</code>
          </li>
          <li>
            <code>left_rotate()</code> / <code>right_rotate()</code>: local
            restructuring that preserves in-order key ordering
          </li>
          <li>
            <code>NIL</code> sentinel node: a single shared “leaf” node that
            simplifies edge-case logic (children are never <code>null</code>)
          </li>
        </ul>

        <p>
          If you’re learning RB trees, a useful exercise is to set breakpoints in
          <code>_insert_fixup()</code> and watch how recoloring/rotations prevent
          red-red violations and keep black-heights consistent.
        </p>

        <CodeBlock
          title="Red-Black Tree implementation"
          filename="algorithms/epoll-rbtree/rbtree.py"
          code={rbTreeCode}
          runSnippet={rbTreeRun}
        />
      </Section>

      <Section title="EpollRB: a user-space model of epoll">
        <p>
          The <code>EpollRB</code> class glues the RB-tree (interest set) to the
          deque (ready list) and exposes an API that mirrors the “shape” of real
          epoll usage.
        </p>

        <p>
          Think of each method as mapping to what you’d do with a real epoll fd:
        </p>

        <ul>
          <li>
            <code>register(fd, events, data=None)</code>:
            add or overwrite an interest entry
          </li>
          <li>
            <code>modify(fd, events, data=None)</code>:
            update the mask and/or user payload for an existing entry
          </li>
          <li>
            <code>unregister(fd)</code>:
            remove the interest entry (and stop getting readiness notifications)
          </li>
          <li>
            <code>trigger(fd, event_mask)</code>:
            simulate readiness being observed by the kernel
          </li>
          <li>
            <code>wait(timeout, maxevents)</code>:
            pull readiness notifications out of the ready list
          </li>
        </ul>

        <p>
          The demo in <code>if __name__ == "__main__":</code> shows the typical
          flow:
        </p>

        <ol>
          <li>register fake fds + masks</li>
          <li>simulate readiness via <code>trigger()</code></li>
          <li>retrieve ready events via <code>wait()</code></li>
        </ol>

        <p>
          A subtle learning point: the event returned is the event that became
          ready (<code>event_mask</code>), but it’s only returned because it
          overlapped the registered interest mask. That’s why fd 11’s writable
          event is ignored in the example: it wasn’t in the interest set.
        </p>

        <CodeBlock
          title="EpollRB: epoll modeled with an RB-tree"
          filename="algorithms/epoll-rbtree/epoll_rbtree.py"
          code={epollRbCode}
          supportingFiles={[{ filename: "rbtree.py", code: rbTreeCode }]}
          runSnippet={epollRun}
        />
      </Section>

      <Section title="Suggested learning exercises">
        <div className="cards-grid">
          <ConceptCard title="Exercise 1: add a range query to the RBTree">
            <p>
              Add a method that returns all keys in <code>[lo, hi]</code>. This
              demonstrates why ordered structures are useful beyond mere lookup.
            </p>
          </ConceptCard>

          <ConceptCard title="Exercise 2: deduplicate the ready queue">
            <p>
              Real systems often avoid enqueuing duplicate readiness notifications
              for the same fd. Add a “ready set” alongside the deque to prevent
              duplicates, and remove from the set when popped.
            </p>
          </ConceptCard>

          <ConceptCard title="Exercise 3: level-triggered behavior">
            <p>
              In level-triggered mode, if an fd stays readable, it should keep
              showing up until you “drain” it. Model that by re-enqueueing after
              <code>wait()</code> unless a simulated “drain” call clears it.
            </p>
          </ConceptCard>
        </div>
      </Section>
    </div>
  );
}

export default EpollPage;
