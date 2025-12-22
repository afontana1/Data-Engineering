import type { FC } from 'react'
import type { SolverMethod } from '../faulttree/types'

type Props = {
  topEventId: string
  setTopEventId: (v: string) => void
  solver: SolverMethod
  setSolver: (v: SolverMethod) => void
  missionTimeHours: number | null
  setMissionTimeHours: (v: number | null) => void

  nodeIds: string[]
  onAddBasic: () => void
  onAddHouse: () => void
  onAddGate: () => void
  onAddCCF: () => void
  onAddFDEP: () => void
  onSolve: () => void
  solving: boolean
}

export const Toolbar: FC<Props> = (p) => {
  return (
    <div className="header">
      <h1>Fault Tree Builder</h1>

      <div className="row" style={{ margin: 0, width: 320 }}>
        <label style={{ width: 90 }}>Top Event</label>
        <select value={p.topEventId} onChange={(e) => p.setTopEventId(e.target.value)}>
          <option value="">(select)</option>
          {p.nodeIds.map((id) => (
            <option key={id} value={id}>{id}</option>
          ))}
        </select>
      </div>

      <div className="row" style={{ margin: 0, width: 260 }}>
        <label style={{ width: 70 }}>Solver</label>
        <select value={p.solver} onChange={(e) => p.setSolver(e.target.value as SolverMethod)}>
          <option value="bdd_exact">bdd_exact</option>
          <option value="monte_carlo">monte_carlo</option>
          <option value="closed_form">closed_form</option>
          <option value="cut_sets">cut_sets</option>
          <option value="rare_event">rare_event</option>
        </select>
      </div>

      <div className="row" style={{ margin: 0, width: 240 }}>
        <label style={{ width: 120 }}>Mission (hrs)</label>
        <input
          type="number"
          step="0.1"
          placeholder="optional"
          value={p.missionTimeHours ?? ''}
          onChange={(e) => p.setMissionTimeHours(e.target.value === '' ? null : Number(e.target.value))}
        />
      </div>

      <div className="spacer" />

      <button onClick={p.onAddBasic}>+ Basic</button>
      <button onClick={p.onAddHouse}>+ House</button>
      <button onClick={p.onAddGate}>+ Gate</button>
      <button onClick={p.onAddCCF}>+ CCF</button>
      <button onClick={p.onAddFDEP}>+ FDEP</button>

      <button className="primary" onClick={p.onSolve} disabled={p.solving || !p.topEventId}>
        {p.solving ? 'Solving…' : 'Solve'}
      </button>
    </div>
  )
}
