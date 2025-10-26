// ============================================
// CONDA Design System - Vite Configuration
// Modern build system with optimization
// ============================================

import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  // Build configuration
  build: {
    lib: {
      entry: {
        'conda-design-system': resolve(__dirname, 'src/styles/conda-design-system.css'),
        'conda-themes': resolve(__dirname, 'src/styles/conda-themes.css'),
        'conda-components': resolve(__dirname, 'src/components/index.js'),
        'theme-switcher': resolve(__dirname, 'src/utils/theme-switcher.js'),
        'conda-config': resolve(__dirname, 'src/utils/conda-config.js'),
      },
      formats: ['es', 'umd'],
      name: 'CONDA',
    },
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
      format: {
        comments: false,
      },
    },
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name.endsWith('.css')) {
            return 'css/[name].[hash].css';
          }
          return 'assets/[name].[hash][extname]';
        },
        chunkFileNames: 'js/[name].[hash].js',
        entryFileNames: 'js/[name].[hash].js',
      },
    },
    cssCodeSplit: true,
    cssMinify: true,
  },
  
  // CSS configuration
  css: {
    postcss: {
      plugins: [
        {
          postcssPlugin: 'internal:charset-removal',
          AtRule: {
            charset: (atRule) => {
              if (atRule.name === 'charset') {
                atRule.remove();
              }
            },
          },
        },
      ],
    },
    preprocessorOptions: {
      css: {
        charset: false,
      },
    },
  },
  
  // Server configuration for development
  server: {
    port: 3000,
    open: true,
    cors: true,
    hmr: {
      overlay: true,
    },
  },
  
  // Preview server configuration
  preview: {
    port: 8080,
    open: true,
  },
  
  // Optimization
  optimizeDeps: {
    include: [],
  },
  
  // Define global constants
  define: {
    __VERSION__: JSON.stringify(process.env.npm_package_version || '1.0.0'),
    __DEV__: process.env.NODE_ENV !== 'production',
  },
});
