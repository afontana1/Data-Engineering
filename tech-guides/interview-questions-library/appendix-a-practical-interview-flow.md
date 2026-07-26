# A practical interview flow

Instead of asking from every category, you can get a lot of signal with a sequence like this:

1. Start with context

   * What problem was the system solving, for whom, and what constraints mattered most?

2. Move to architecture

   * Walk me through the high-level design and the top tradeoffs.

3. Force scale/design linkage

   * What assumptions about load, growth, or usage shaped the design?

4. Pick one deep technical area

   * Data model, APIs, async processing, frontend/backend boundary, or performance.

5. Probe failure and resilience

   * What were the main failure modes and how did you handle them?

6. Probe patterns and abstraction

   * What recurring concern or abstraction did you handle especially thoughtfully, and why?

7. End with evolution

   * What changed over time, and what would you redesign now?

That usually gets much more signal than a broad but shallow tour.

---

## A compact “high-signal” shortlist

If you only have limited time, these are especially revealing:

* What problem was this system solving, and what constraints mattered most?
* What were the top two or three design decisions that shaped everything else?
* What assumptions about scale or usage influenced the design?
* What alternatives did you consider, and why did you reject them?
* What was the hardest invariant or correctness property to maintain?
* What were the most important failure modes?
* What cross-cutting concern showed up repeatedly, and how did you handle it?
* What did you intentionally not build or not abstract?
* How did the system need to evolve after the first version?
* What would you redesign now, and why?

---

## What strong answers tend to sound like

You are probably looking for answers that naturally include things like:

* explicit tradeoffs
* user or business context
* constraint-awareness
* failure-aware thinking
* discussion of alternatives
* awareness of coupling and boundaries
* evolution over time
* reasoning about “why,” not just “what”
* ownership of decisions and mistakes

Weak answers tend to sound like:

* feature walkthroughs without design rationale
* naming technologies instead of explaining decisions
* no mention of constraints, risks, or alternatives
* no awareness of failure modes
* inability to connect implementation details back to system goals

When they answer, keep pulling with:

* “What drove that choice?”
* “What was the tradeoff?”
* “What would break first?”
* “What changed your mind?”
* “What did that buy you?”

Those follow-ups often expose systems thinking faster than entirely new questions.

Above are oriented towards a general understanding of system design. The next few are more specific.

---
