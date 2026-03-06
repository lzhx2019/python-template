/** 用户信息 */
export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
}

/** 登录成功后返回的令牌 */
export interface TokenResponse {
  access_token: string
  token_type: string
}

/** 登录请求参数 */
export interface LoginParams {
  username: string
  password: string
}

/** 注册请求参数 */
export interface RegisterParams {
  username: string
  email: string
  password: string
}
