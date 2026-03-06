/**
 * 根组件：配置客户端路由。
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from '@/components/Layout'
import Home from '@/pages/Home'
import Login from '@/pages/Login'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 公共布局：所有页面共享 */}
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
