import { Outlet } from 'react-router-dom'
import styles from './index.module.less'

export default function Layout() {
  return (
    <div className={styles.layout}>
      <Outlet />
    </div>
  )
}
