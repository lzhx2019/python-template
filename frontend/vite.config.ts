/**
 * Vite 构建配置
 */
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],

  resolve: {
    // 路径别名：@ 指向 src 目录
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },

  css: {
    preprocessorOptions: {
      // 启用 Less 的 JavaScript 表达式支持
      less: {
        javascriptEnabled: true,
      },
    },
  },

  server: {
    port: 5173,
    // 开发代理：将 /api 请求转发到后端服务
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
