/**
 * 首页：展示欢迎信息，已登录用户显示用户名和登出按钮。
 */
import { useAuthStore } from '@/stores/useAuthStore'
import styles from './index.module.less'

export default function Home() {
  const { user, logout } = useAuthStore()

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Welcome to the App</h1>
        {user ? (
          <div className={styles.userInfo}>
            <span>Hello, {user.username}</span>
            <button onClick={logout}>Logout</button>
          </div>
        ) : (
          <a href="/login">Login</a>
        )}
      </header>
      <main className={styles.main}>
        <p>Your full-stack project is ready.</p>
      </main>
    </div>
  )
}
