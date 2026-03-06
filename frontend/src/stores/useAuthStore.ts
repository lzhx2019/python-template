/**
 * 认证状态管理（Zustand）：管理令牌、用户信息、登录/登出操作。
 */
import { create } from 'zustand'
import type { User } from '@/types'
import request from '@/utils/request'

/** 认证状态接口定义 */
interface AuthState {
  token: string | null
  user: User | null
  loading: boolean
  setToken: (token: string | null) => void
  fetchUser: () => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  // 初始化时从 localStorage 读取已有令牌
  token: localStorage.getItem('token'),
  user: null,
  loading: false,

  /** 设置令牌并同步到 localStorage */
  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
    set({ token })
  },

  /** 调用接口获取当前用户信息 */
  fetchUser: async () => {
    set({ loading: true })
    try {
      const user = await request.get<unknown, User>('/auth/me')
      set({ user, loading: false })
    } catch {
      set({ user: null, loading: false })
    }
  },

  /** 登出：清除令牌和用户信息 */
  logout: () => {
    localStorage.removeItem('token')
    set({ token: null, user: null })
  },
}))
