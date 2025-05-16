import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    port: 5555,
    host: true,
    strictPort: true
  },
  preview: {
    host: true,
    port: 5556
  },
  esbuild: {
    loader: 'jsx', // Correctly specify 'jsx' for files with JSX syntax
    include: /\.jsx?$/, // Include both .js and .jsx files
  },
  plugins: [
    react(),
    {
      name: 'debug-plugin',
      transform(code, id) {
        console.log(`[vite-debug] transforming: ${id}`);
        return null;
      }
    }
  ]
});
