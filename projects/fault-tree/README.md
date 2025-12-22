# faulttree

Static fault-tree primitives + solvers + FastAPI app.

## Run the API
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[dev]"
python -m pytest -q
uvicorn app.main:app --reload
```

## Run Front end

```bash
npm install
npm run dev
```

## Examples

```bash
# --- Health check ---
# Expected: {"ok":true}
curl http://127.0.0.1:8000/health


# --- Get the JSON Schema for the FaultTree DSL ---
# Expected: a JSON schema document (large) describing valid config fields/types
curl http://127.0.0.1:8000/schema/faulttree


# --- Solve: BDD exact (recommended default) ---
# Model: TOP = A OR B where P(A)=0.1, P(B)=0.2
# Expected: top_event_probability = 0.28 (since 0.1 + 0.2 - 0.1*0.2 = 0.28)
# Response shape: {"method":"bdd_exact","top_event_probability":0.28,"details":{...}}
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"metadata\": {\"example\": true}, \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"A\", \"name\": \"A fails\", \"p\": 0.1}, {\"kind\": \"basic_event\", \"id\": \"B\", \"name\": \"B fails\", \"p\": 0.2}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"or\", \"inputs\": [\"A\", \"B\"]} ] }, \"method\": \"bdd_exact\" }"


# --- Solve: Monte Carlo (with seed + sample count) ---
# Same model as above (TOP = A OR B, P(A)=0.1, P(B)=0.2)
# Expected: top_event_probability close to 0.28 (e.g., ~0.279–0.281) with a 95% CI in details
# Response details include: {"samples":200000,"hits":...,"ci95":[lo,hi],...}
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"A\", \"name\": \"A fails\", \"p\": 0.1}, {\"kind\": \"basic_event\", \"id\": \"B\", \"name\": \"B fails\", \"p\": 0.2}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"or\", \"inputs\": [\"A\", \"B\"]} ] }, \"method\": \"monte_carlo\", \"mc_samples\": 200000, \"mc_seed\": 123 }"


# --- Solve: Closed-form (tree-only; fails if you have shared events) ---
# Model: TOP = A AND B with P(A)=0.1, P(B)=0.2
# Expected: top_event_probability = 0.02 (since 0.1 * 0.2 = 0.02)
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"A\", \"name\": \"A fails\", \"p\": 0.1}, {\"kind\": \"basic_event\", \"id\": \"B\", \"name\": \"B fails\", \"p\": 0.2}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"and\", \"inputs\": [\"A\", \"B\"]} ] }, \"method\": \"closed_form\" }"


# --- Solve: Cut sets (returns minimal cut sets + rare-event approximation in details) ---
# Model: TOP = (A AND B) OR C with P(A)=0.001, P(B)=0.002, P(C)=0.003
# Minimal cut sets expected: ["A","B"] and ["C"]
# Rare-event approx expected: P(TOP) ≈ P(A)*P(B) + P(C) = 0.000002 + 0.003 = 0.003002
# Response details include: "cut_sets": [["C"],["A","B"]] (order may differ)
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"A\", \"name\": \"A fails\", \"p\": 0.001}, {\"kind\": \"basic_event\", \"id\": \"B\", \"name\": \"B fails\", \"p\": 0.002}, {\"kind\": \"basic_event\", \"id\": \"C\", \"name\": \"C fails\", \"p\": 0.003}, {\"kind\": \"gate\", \"id\": \"G1\", \"name\": \"A and B\", \"gate_type\": \"and\", \"inputs\": [\"A\", \"B\"]}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"or\", \"inputs\": [\"G1\", \"C\"]} ] }, \"method\": \"cut_sets\", \"max_cut_sets\": 10000, \"max_cut_set_order\": 10 }"


# --- Solve: Inhibit gate (AND(primary..., condition)) ---
# Model: TOP = LOSS_FLOW AND MAINT_MODE, where LOSS_FLOW has p=0.01 and MAINT_MODE is a HouseEvent
# Here we override MAINT_MODE=true, so expected: P(TOP) = 0.01
# If MAINT_MODE=false, expected: P(TOP) = 0.0
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"LOSS_FLOW\", \"name\": \"Loss of flow\", \"p\": 0.01}, {\"kind\": \"house_event\", \"id\": \"MAINT_MODE\", \"name\": \"Maintenance mode\", \"value\": false}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"inhibit\", \"inputs\": [\"LOSS_FLOW\", \"MAINT_MODE\"]} ] }, \"method\": \"bdd_exact\", \"house_overrides\": {\"MAINT_MODE\": true} }"


# --- Solve: k-out-of-n voting gate (k=2 of 3) ---
# Model: TOP = (at least 2 of {CH1,CH2,CH3}) with each p=0.01 independent
# Expected: P(TOP) = 3*p^2*(1-p) + p^3
#          = 3*(0.0001)*0.99 + 0.000001
#          = 0.000297 + 0.000001 = 0.000298
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"CH1\", \"name\": \"Channel 1\", \"p\": 0.01}, {\"kind\": \"basic_event\", \"id\": \"CH2\", \"name\": \"Channel 2\", \"p\": 0.01}, {\"kind\": \"basic_event\", \"id\": \"CH3\", \"name\": \"Channel 3\", \"p\": 0.01}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"2oo3 fails\", \"gate_type\": \"kofn\", \"k\": 2, \"inputs\": [\"CH1\", \"CH2\", \"CH3\"]} ] }, \"method\": \"bdd_exact\" }"


# --- Solve: Common Cause Failure group (beta factor) ---
# Model: TOP = CH1 AND CH2, with each channel p=0.01 and CCF beta=0.1
# This backend expands CCF into latent independent vars:
#   common = beta*q = 0.1*0.01 = 0.001
#   ind_i  = (1-beta)*q = 0.9*0.01 = 0.009
#   CHi := common OR ind_i
# Expected: each CHi has P(CHi)=1-(1-0.001)*(1-0.009)=0.009991
# Expected: P(TOP)=P(CH1 AND CH2)=P(common OR ind1) * P(common OR ind2) with shared common
# Exact value under this expansion:
#   P(TOP) = P(common) + (1-P(common))*P(ind1)*P(ind2)
#          = 0.001 + 0.999*(0.009*0.009)
#          = 0.001 + 0.999*0.000081 = 0.001080919
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"CH1\", \"name\": \"Channel 1 fails\", \"p\": 0.01}, {\"kind\": \"basic_event\", \"id\": \"CH2\", \"name\": \"Channel 2 fails\", \"p\": 0.01}, {\"kind\": \"ccf_group\", \"id\": \"CCF1\", \"name\": \"Channels 1-2 CCF\", \"members\": [\"CH1\", \"CH2\"], \"beta\": 0.1}, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"and\", \"inputs\": [\"CH1\", \"CH2\"]} ] }, \"method\": \"bdd_exact\" }"


# --- Solve: Functional dependency (if TRIGGER then DEPENDENT occurs) ---
# Model: FDEP forces DEP := DEP OR TRIG
# Top: TOP = DEP
# With P(TRIG)=0.05, P(DEP)=0.01 independent
# Expected: P(TOP)=P(DEP OR TRIG)=0.01 + 0.05 - 0.01*0.05 = 0.0595
curl -X POST http://127.0.0.1:8000/solve ^
  -H "Content-Type: application/json" ^
  -d "{ \"config\": { \"version\": \"1.0\", \"top_event_id\": \"TOP\", \"nodes\": [ {\"kind\": \"basic_event\", \"id\": \"TRIG\", \"name\": \"Trigger fails\", \"p\": 0.05}, {\"kind\": \"basic_event\", \"id\": \"DEP\", \"name\": \"Dependent fails\", \"p\": 0.01}, {\"kind\": \"fdep\", \"id\": \"FD1\", \"name\": \"TRIG forces DEP\", \"trigger\": \"TRIG\", \"dependent\": \"DEP\" }, {\"kind\": \"gate\", \"id\": \"TOP\", \"name\": \"Top event\", \"gate_type\": \"or\", \"inputs\": [\"DEP\"]} ] }, \"method\": \"bdd_exact\" }"
```