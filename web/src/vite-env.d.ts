/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
  readonly VITE_MOCK?: string
  readonly VITE_MOCK_SPEED?: string
}
interface ImportMeta { readonly env: ImportMetaEnv }

declare module '*.html?raw' { const s: string; export default s }
