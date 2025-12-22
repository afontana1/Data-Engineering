import type { Edge, Node } from '@xyflow/react'
import type { FaultTreeConfig, NodeCfg, PrimitiveKind, GateType } from './types'

export type UIData = {
  kind: PrimitiveKind
  name: string

  // basic
  p?: number | null
  lambda_rate_per_hour?: number | null

  // house
  value?: boolean | null

  // gate
  gate_type?: GateType
  k?: number | null
  inhibit_condition?: string | null

  // ccf
  beta?: number
  members?: string[]

  // fdep
  trigger?: string | null
  dependent?: string | null
}

function incomingSources(edges: Edge[], targetId: string): string[] {
  return edges.filter(e => e.target === targetId).map(e => String(e.source))
}

export function buildFaultTreeConfig(params: {
  nodes: Node<UIData>[]
  edges: Edge[]
  topEventId: string
}): FaultTreeConfig {
  const { nodes, edges, topEventId } = params

  const cfgNodes: NodeCfg[] = nodes.map((n) => {
    const id = String(n.id)
    const d = n.data

    if (d.kind === 'basic_event') {
      return {
        kind: 'basic_event',
        id,
        name: d.name ?? id,
        p: d.p ?? null,
        lambda_rate_per_hour: d.lambda_rate_per_hour ?? null,
      }
    }

    if (d.kind === 'house_event') {
      return {
        kind: 'house_event',
        id,
        name: d.name ?? id,
        value: d.value ?? null,
      }
    }

    if (d.kind === 'gate') {
      const gateType = d.gate_type ?? 'or'
      let inputs = incomingSources(edges, id)

      if (gateType === 'inhibit' && inputs.length >= 2) {
        // Convention required by backend: last input is the condition
        const cond = d.inhibit_condition ?? inputs[inputs.length - 1]
        const primaries = inputs.filter(x => x !== cond)
        inputs = [...primaries, cond]
      }

      return {
        kind: 'gate',
        id,
        name: d.name ?? id,
        gate_type: gateType,
        inputs,
        k: gateType === 'kofn' ? (d.k ?? 2) : null,
      }
    }

    if (d.kind === 'ccf_group') {
      return {
        kind: 'ccf_group',
        id,
        name: d.name ?? id,
        members: d.members ?? [],
        beta: d.beta ?? 0.1,
      }
    }

    // fdep
    return {
      kind: 'fdep',
      id,
      name: d.name ?? id,
      trigger: d.trigger ?? '',
      dependent: d.dependent ?? '',
    }
  })

  return {
    version: '1.0',
    metadata: { generatedBy: 'frontend' },
    top_event_id: topEventId,
    nodes: cfgNodes,
  }
}
