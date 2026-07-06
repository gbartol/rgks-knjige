import { useAuth } from './auth/useAuth'
import type { Profile, UserSummary, Book, Shelf, Review } from './types' 

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

export async function searchBooks(query: string) {
  const token = await getApiToken()
  const resp = await fetch(`/api/books/search/?q=${encodeURIComponent(query)}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function fetchBookDetail(externalId: string) {
  const token = await getApiToken()
  const resp = await fetch(`/api/books/${externalId}/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function addReview(externalId: string, reviewData: { rating: number; text: string }) {
  const token = await getApiToken()
  const resp = await fetch(`/api/books/${externalId}/reviews/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(reviewData),
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function fetchShelves() {
  const token = await getApiToken()
  const resp = await fetch('/api/shelves/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function createShelf(shelfData: { name: string; is_public?: boolean }) {
  const token = await getApiToken()
  const resp = await fetch('/api/shelves/', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(shelfData),
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function modifyShelfBooks(shelfId: number, action: 'add' | 'remove', externalId: string) {
  const token = await getApiToken()
  const resp = await fetch(`/api/shelves/${shelfId}/${action}/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ external_id: externalId }),
  })
  await throwIfError(resp)
  return await resp.json()
}

export async function deleteReview(reviewId: number) {
  const token = await getApiToken()
  const resp = await fetch(`/api/reviews/${reviewId}/`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
  await throwIfError(resp)
  return true
}