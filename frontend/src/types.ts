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
