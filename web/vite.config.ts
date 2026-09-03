import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The Analyst — web front end. API base comes from VITE_API_BASE (see
// src/lib/api.ts); no dev proxy so the same build talks to Render or to a
// local uvicorn on :8013. Mock mode (VITE_MOCK=1 or ?mock=1) needs no server.
export default defineConfig({
  plugins: [react()],
  server: { port: 5174, host: '127.0.0.1' },
  build: { outDir: 'dist', sourcemap: false },
})
