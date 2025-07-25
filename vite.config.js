import { defineConfig } from 'vite';

export default defineConfig({
  root: 'frontend',
  server: {
    port: 4269,
    open: false,
  },
  build: {
    outDir: '../dist',
    emptyOutDir: true
  }
});