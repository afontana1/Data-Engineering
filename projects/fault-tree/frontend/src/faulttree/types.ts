export type PrimitiveKind = 'basic_event' | 'house_event' | 'gate' | 'ccf_group' | 'fdep'
export type GateType = 'or' | 'and' | 'kofn' | 'inhibit'

export type SolverMethod =
  | 'closed_form'
  | 'cut_sets'
  | 'rare_event'
  | 'bdd_exact'
  | 'monte_carlo'

export type BasicEventCfg = {
  kind: 'basic_event'
  id: string
  name: string
  p?: number | null
  lambda_rate_per_hour?: number | null
}

export type HouseEventCfg = {
  kind: 'house_event'
  id: string
  name: string
  value?: boolean | null
}

export type GateCfg = {
  kind: 'gate'
  id: string
  name: string
  gate_type: GateType
  inputs: string[]
  k?: number | null
}

export type CCFGroupCfg = {
  kind: 'ccf_group'
  id: string
  name: string
  members: string[]
  beta: number
}

export type FDepCfg = {
  kind: 'fdep'
  id: string
  name: string
  trigger: string
  dependent: string
}

export type NodeCfg = BasicEventCfg | HouseEventCfg | GateCfg | CCFGroupCfg | FDepCfg

export type FaultTreeConfig = {
  version: '1.0'
  metadata?: Record<string, unknown>
  top_event_id: string
  nodes: NodeCfg[]
}

export type SolveRequestBody = {
  config: FaultTreeConfig
  method: SolverMethod
  mission_time_hours?: number | null
  house_overrides?: Record<string, boolean> | null
  prob_overrides?: Record<string, number> | null
  max_cut_sets?: number
  max_cut_set_order?: number
  mc_samples?: number
  mc_seed?: number | null
}

export type SolveResponseBody = {
  method: SolverMethod
  top_event_probability: number
  details: Record<string, unknown>
}
