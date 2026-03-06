/**
 * 全局布局组件：包裹所有页面，通过 Outlet 渲染子路由。
 */
import { Outlet } from 'react-router-dom'
import styles from './index.module.less'

export default function Layout() {
  return (
    <div className={styles.layout}>
      <Outlet />
    </div>
  )
}
