import type { SolveRequestBody, SolveResponseBody } from './faulttree/types'

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'

export async function solveFaultTree(body: SolveRequestBody): Promise<SolveResponseBody> {
  const res = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Solve failed (${res.status}): ${text}`)
  }

  return await res.json()
}
