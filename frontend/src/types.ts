export type UserSummary = {
  id: number
  username: string
  display_name: string
  avatar_url: string | null
  is_following?: boolean // popunjeno kad gledamo drugog korisnika
}

export type Profile = {
  display_name: string
  avatar_url: string | null
}

export interface Book {
  id: number
  external_id: string
  isbn: string | null
  title: string
  authors: string
  description: string | null
  cover_url: string | null
  published_year: number | null
}

export interface Shelf {
  id: number
  name: string
  is_system: boolean
  is_public: boolean
  books_count: number
  books?: Book[] // Opcionalno, ovisno šalješ li odmah i niz knjiga
}

export interface Review {
  id: number
  user: UserSummary
  book: { id: number; title: string; authors: string; cover_url: string | null }
  rating: number
  text: string
  created_at: string
}
