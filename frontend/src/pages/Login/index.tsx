/**
 * 登录页：输入用户名和密码，调用后端接口获取 JWT 令牌。
 */
import { type FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/useAuthStore'
import request from '@/utils/request'
import type { TokenResponse } from '@/types'
import styles from './index.module.less'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { setToken, fetchUser } = useAuthStore()

  /** 提交登录表单 */
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const data = await request.post<unknown, TokenResponse>('/auth/login', {
        username,
        password,
      })
      setToken(data.access_token)
      await fetchUser()
      navigate('/')
    } catch {
      setError('Invalid username or password')
    }
  }

  return (
    <div className={styles.wrapper}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2>Login</h2>
        {error && <p className={styles.error}>{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Sign In</button>
        <p className={styles.link}>
          Don&apos;t have an account? <a href="/register">Register</a>
        </p>
      </form>
    </div>
  )
}
