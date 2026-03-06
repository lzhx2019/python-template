/// <reference types="vite/client" />

/** 声明 Less CSS Modules 的类型，使 TypeScript 正确识别 *.module.less 导入 */
declare module '*.module.less' {
  const classes: { readonly [key: string]: string }
  export default classes
}
