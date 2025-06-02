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
    loader: 'tsx', // Correctly specify 'jsx' for files with JSX syntax
    include: /\.[jt]sx?$/, // Include both .js,.jsx,.ts,.tsx files
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
