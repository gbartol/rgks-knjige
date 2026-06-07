import { useAuth } from './auth/useAuth'
import type { Profile, UserSummary } from './types'

const { getApiToken } = useAuth()


export class ValidationError extends Error {
  constructor(public fields: Record<string, string[]>) {
    super('Validation error')
  }
}

async function throwIfError(response: Response) {
  if (response.ok) return
  let body
  try {
    body = await response.json()
  } catch {
    throw new Error(`${response.status} ${response.statusText}`)
  }
  if (response.status === 400) throw new ValidationError(body)
  throw new Error(body.detail ?? `${response.status} ${response.statusText}`)
}

export function formatError(err: unknown) {
  if (err instanceof ValidationError) {
    return Object.entries(err.fields)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('\n')
  }
  return err instanceof Error ? err.message : String(err)
}

//------ API pozivi -------
export async function fetchMyProfile() {
  const token = await getApiToken()
  const resp = await fetch('/api/profile/me/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  await throwIfError(resp)
  return await resp.json() as Profile
}

export async function updateMyProfile(changes: Partial<Profile>) {
  const token = await getApiToken()
  const resp = await fetch('/api/profile/me/', {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(changes),
  })
  await throwIfError(resp)
  return await resp.json() as Profile
}

export async function userSearch(search: string) {
    const token = await getApiToken()
    const resp = await fetch(`/api/users/?search=${encodeURIComponent(search)}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    await throwIfError(resp)
    const data = await resp.json()
    return data.results as UserSummary[]
}
