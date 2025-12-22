import type { FC } from 'react'
import type { SolveRequestBody, SolveResponseBody } from '../faulttree/types'

type Props = {
  payload: SolveRequestBody | null
  result: SolveResponseBody | null
  error: string | null
}

export const ResultsPanel: FC<Props> = ({ payload, result, error }) => {
  return (
    <div className="panel">
      <h2>Model Results</h2>

      {error && (
        <>
          <div className="small" style={{ color: '#b91c1c' }}><b>Error</b></div>
          <pre>{error}</pre>
        </>
      )}

      <div className="small"><b>Payload</b> (sent to backend)</div>
      <pre>{payload ? JSON.stringify(payload, null, 2) : '{ }'}</pre>

      <div className="small"><b>Response</b></div>
      <pre>{result ? JSON.stringify(result, null, 2) : '{ }'}</pre>
    </div>
  )
}
