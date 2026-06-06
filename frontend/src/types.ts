export type UserSummary = {
  id: number
  username: string
  displayName: string
  avatarUrl: string | null
  isFollowing?: boolean // popunjeno kad gledamo drugog korisnika
}

export type Profile = {
  user: UserSummary
  displayName: string
  avatarUrl: string | null
}
