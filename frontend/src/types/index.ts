export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
}
