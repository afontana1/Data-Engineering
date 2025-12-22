import { useCallback, useMemo, useState } from 'react'
import {
  ReactFlow,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Background,
  Controls,
  type Node,
  type Edge,
  type Connection,
  type NodeTypes,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'

import { Toolbar } from './components/Toolbar'
import { Inspector } from './components/Inspector'
import { ResultsPanel } from './components/ResultsPanel'
import { PrimitiveNode } from './components/PrimitiveNode'

import type { SolverMethod, SolveRequestBody, SolveResponseBody } from './faulttree/types'
import { buildFaultTreeConfig, type UIData } from './faulttree/buildConfig'
import { solveFaultTree } from './api'

let idCounter = 1
function nextId(prefix: string) {
  return `${prefix}_${idCounter++}`
}

export default function App() {
  const [nodes, setNodes] = useState<Node<UIData>[]>([])
  const [edges, setEdges] = useState<Edge[]>([])

  const [topEventId, setTopEventId] = useState<string>('')
  const [solver, setSolver] = useState<SolverMethod>('bdd_exact')
  const [missionTimeHours, setMissionTimeHours] = useState<number | null>(null)

  const [payload, setPayload] = useState<SolveRequestBody | null>(null)
  const [result, setResult] = useState<SolveResponseBody | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [solving, setSolving] = useState(false)

  const [selectedId, setSelectedId] = useState<string | null>(null)

  const nodeTypes: NodeTypes = useMemo(() => ({ primitive: PrimitiveNode }), [])

  const selected = useMemo(
    () => (selectedId ? nodes.find(n => String(n.id) === selectedId) ?? null : null),
    [nodes, selectedId]
  )

  const nodeIds = useMemo(() => nodes.map(n => String(n.id)), [nodes])

  const onNodesChange = useCallback((changes: any) => {
    setNodes((nds) => applyNodeChanges(changes, nds))
  }, [])

  const onEdgesChange = useCallback((changes: any) => {
    setEdges((eds) => applyEdgeChanges(changes, eds))
  }, [])

  const onConnect = useCallback((c: Connection) => {
    setEdges((eds) => addEdge({ ...c }, eds))
  }, [])

  const onSelectionChange = useCallback((sel: any) => {
    const first = sel?.nodes?.[0]
    setSelectedId(first ? String(first.id) : null)
  }, [])

  const addNode = useCallback((kind: UIData['kind']) => {
    const id =
      kind === 'basic_event' ? nextId('BE') :
      kind === 'house_event' ? nextId('HE') :
      kind === 'gate' ? nextId('G') :
      kind === 'ccf_group' ? nextId('CCF') :
      nextId('FDEP')

    const base: UIData = { kind, name: id }

    const data: UIData =
      kind === 'basic_event' ? { ...base, p: 0.01 } :
      kind === 'house_event' ? { ...base, value: null } :
      kind === 'gate' ? { ...base, gate_type: 'or', k: 2, inhibit_condition: null } :
      kind === 'ccf_group' ? { ...base, beta: 0.1, members: [] } :
      { ...base, trigger: null, dependent: null }

    const x = 40 + Math.random() * 250
    const y = 40 + Math.random() * 250

    setNodes((nds) => nds.concat({
      id,
      type: 'primitive',
      position: { x, y },
      data,
    }))
  }, [])

  const onUpdateNode = useCallback((id: string, patch: Partial<UIData>) => {
    setNodes((nds) =>
      nds.map((n) => (String(n.id) === id ? { ...n, data: { ...n.data, ...patch } } : n)),
    )
  }, [])

  const onSolve = useCallback(async () => {
    setError(null)
    setResult(null)

    if (!topEventId) {
      setError('Select a top_event_id first.')
      return
    }

    const config = buildFaultTreeConfig({ nodes, edges, topEventId })

    const body: SolveRequestBody = {
      config,
      method: solver,
      mission_time_hours: missionTimeHours,
      // you can add overrides in the UI later; keeping minimal for now
      max_cut_sets: 50_000,
      max_cut_set_order: 20,
      mc_samples: 50_000,
      mc_seed: 123,
    }

    setPayload(body)
    setSolving(true)
    try {
      const res = await solveFaultTree(body)
      setResult(res)
    } catch (e: any) {
      setError(String(e?.message ?? e))
    } finally {
      setSolving(false)
    }
  }, [topEventId, nodes, edges, solver, missionTimeHours])

  return (
    <div className="app">
      <Toolbar
        topEventId={topEventId}
        setTopEventId={setTopEventId}
        solver={solver}
        setSolver={setSolver}
        missionTimeHours={missionTimeHours}
        setMissionTimeHours={setMissionTimeHours}
        nodeIds={nodeIds}
        onAddBasic={() => addNode('basic_event')}
        onAddHouse={() => addNode('house_event')}
        onAddGate={() => addNode('gate')}
        onAddCCF={() => addNode('ccf_group')}
        onAddFDEP={() => addNode('fdep')}
        onSolve={onSolve}
        solving={solving}
      />

      <div className="main">
        <Inspector selected={selected} nodes={nodes} edges={edges} onUpdate={onUpdateNode} />

        <div className="flow-wrap">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onSelectionChange={onSelectionChange}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </div>

        <ResultsPanel payload={payload} result={result} error={error} />
      </div>
    </div>
  )
}
