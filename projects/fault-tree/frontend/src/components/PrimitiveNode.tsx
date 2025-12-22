import type { FC } from 'react'
import type { NodeProps } from '@xyflow/react'
import { Handle, Position } from '@xyflow/react'
import type { UIData } from '../faulttree/buildConfig'

const badge: Record<string, string> = {
  basic_event: 'Basic',
  house_event: 'House',
  gate: 'Gate',
  ccf_group: 'CCF',
  fdep: 'FDEP',
}

export const PrimitiveNode: FC<NodeProps<UIData>> = ({ id, data, selected }) => {
  return (
    <div
      style={{
        padding: 10,
        borderRadius: 12,
        border: selected ? '2px solid #111827' : '1px solid #d1d5db',
        background: 'white',
        minWidth: 160,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
        <div style={{ fontWeight: 700, fontSize: 12 }}>{data.name || id}</div>
        <div style={{ fontSize: 10, color: '#6b7280' }}>{badge[data.kind] ?? data.kind}</div>
      </div>
      <div style={{ marginTop: 6, fontSize: 11, color: '#374151' }}>
        <div><b>id</b>: {id}</div>
        {data.kind === 'gate' && <div><b>type</b>: {data.gate_type ?? 'or'}</div>}
        {data.kind === 'basic_event' && (data.p != null) && <div><b>p</b>: {data.p}</div>}
        {data.kind === 'house_event' && (data.value != null) && <div><b>value</b>: {String(data.value)}</div>}
      </div>

      {/* connections */}
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  )
}
