import type { FC } from 'react'
import type { Node, Edge } from '@xyflow/react'
import type { UIData } from '../faulttree/buildConfig'

type Props = {
  selected: Node<UIData> | null
  nodes: Node<UIData>[]
  edges: Edge[]
  onUpdate: (id: string, patch: Partial<UIData>) => void
}

export const Inspector: FC<Props> = ({ selected, nodes, edges, onUpdate }) => {
  if (!selected) {
    return (
      <div className="panel">
        <h2>Inspector</h2>
        <div className="small">Select a node to edit its properties.</div>
      </div>
    )
  }

  const id = String(selected.id)
  const d = selected.data
  const allIds = nodes.map(n => String(n.id))
  const incoming = edges.filter(e => e.target === id).map(e => String(e.source))

  return (
    <div className="panel">
      <h2>Inspector</h2>
      <div className="small">Editing: <b>{id}</b> ({d.kind})</div>

      <div className="row">
        <label>Name</label>
        <input value={d.name ?? ''} onChange={(e) => onUpdate(id, { name: e.target.value })} />
      </div>

      {d.kind === 'basic_event' && (
        <>
          <div className="row">
            <label>p</label>
            <input
              type="number"
              step="0.000001"
              placeholder="0..1"
              value={d.p ?? ''}
              onChange={(e) => onUpdate(id, { p: e.target.value === '' ? null : Number(e.target.value) })}
            />
          </div>

          <div className="row">
            <label>lambda (/hr)</label>
            <input
              type="number"
              step="0.000001"
              placeholder="optional"
              value={d.lambda_rate_per_hour ?? ''}
              onChange={(e) =>
                onUpdate(id, { lambda_rate_per_hour: e.target.value === '' ? null : Number(e.target.value) })
              }
            />
          </div>

          <div className="small">Tip: backend prefers <b>p</b> if provided; otherwise uses lambda+mission_time.</div>
        </>
      )}

      {d.kind === 'house_event' && (
        <>
          <div className="row">
            <label>value</label>
            <select
              value={d.value === null || d.value === undefined ? '' : String(d.value)}
              onChange={(e) => {
                const v = e.target.value
                onUpdate(id, { value: v === '' ? null : v === 'true' })
              }}
            >
              <option value="">(unset)</option>
              <option value="false">false</option>
              <option value="true">true</option>
            </select>
          </div>
          <div className="small">Unset house events default to false unless you override at solve-time.</div>
        </>
      )}

      {d.kind === 'gate' && (
        <>
          <div className="row">
            <label>gate_type</label>
            <select
              value={d.gate_type ?? 'or'}
              onChange={(e) => onUpdate(id, { gate_type: e.target.value as any })}
            >
              <option value="or">or</option>
              <option value="and">and</option>
              <option value="kofn">kofn</option>
              <option value="inhibit">inhibit</option>
            </select>
          </div>

          {(d.gate_type ?? 'or') === 'kofn' && (
            <div className="row">
              <label>k</label>
              <input
                type="number"
                step="1"
                min="1"
                value={d.k ?? 2}
                onChange={(e) => onUpdate(id, { k: Number(e.target.value) })}
              />
            </div>
          )}

          {(d.gate_type ?? 'or') === 'inhibit' && (
            <>
              <div className="row">
                <label>condition</label>
                <select
                  value={d.inhibit_condition ?? ''}
                  onChange={(e) => onUpdate(id, { inhibit_condition: e.target.value || null })}
                >
                  <option value="">(auto: last input)</option>
                  {incoming.map((src) => (
                    <option key={src} value={src}>{src}</option>
                  ))}
                </select>
              </div>
              <div className="small">
                Inhibit convention: last input is the condition; others are primaries.
              </div>
            </>
          )}

          <div className="small">
            Inputs come from incoming edges. Connect <b>child → gate</b>.
          </div>
        </>
      )}

      {d.kind === 'ccf_group' && (
        <>
          <div className="row">
            <label>beta</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={d.beta ?? 0.1}
              onChange={(e) => onUpdate(id, { beta: Number(e.target.value) })}
            />
          </div>

          <div className="row" style={{ alignItems: 'flex-start' }}>
            <label>members</label>
            <textarea
              rows={4}
              placeholder="one id per line"
              value={(d.members ?? []).join('\n')}
              onChange={(e) =>
                onUpdate(id, { members: e.target.value.split('\n').map(s => s.trim()).filter(Boolean) })
              }
            />
          </div>

          <div className="small">Members should be ids of basic events (channels).</div>
        </>
      )}

      {d.kind === 'fdep' && (
        <>
          <div className="row">
            <label>trigger</label>
            <select
              value={d.trigger ?? ''}
              onChange={(e) => onUpdate(id, { trigger: e.target.value || null })}
            >
              <option value="">(select)</option>
              {allIds.map((x) => <option key={x} value={x}>{x}</option>)}
            </select>
          </div>

          <div className="row">
            <label>dependent</label>
            <select
              value={d.dependent ?? ''}
              onChange={(e) => onUpdate(id, { dependent: e.target.value || null })}
            >
              <option value="">(select)</option>
              {allIds.map((x) => <option key={x} value={x}>{x}</option>)}
            </select>
          </div>

          <div className="small">Backend rewrite: dependent := dependent OR trigger.</div>
        </>
      )}
    </div>
  )
}
