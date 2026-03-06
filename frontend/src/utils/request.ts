/**
 * Axios 请求封装：统一设置基础路径、超时、令牌注入和错误处理。
 */
import axios from 'axios'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000, // 请求超时时间：10 秒
})

// 请求拦截器：自动在请求头中附加 JWT 令牌
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一提取 data 字段，401 时清除令牌并跳转登录页
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export default request
