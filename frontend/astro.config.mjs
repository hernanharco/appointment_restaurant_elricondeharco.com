// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import tailwindcss from '@tailwindcss/vite';
import vercel from '@astrojs/vercel';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  site: 'https://tu-proyectos-saas.com',
  
  integrations: [svelte()],
  
  // Adaptador configurado para Vercel
  adapter: vercel({
    // Opcional: Recomendado para SaaS para ver métricas sin configurar Google Analytics
    webAnalytics: { enabled: true },
  }),
  output: 'server',   

  vite: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    // CLAVE PARA SSR: Evita errores de "Internal Server Error" en Vercel
    // Forzamos a Vite a procesar estas librerías para que sean compatibles con el servidor
    ssr: {
      noExternal: ['lucide-svelte', 'date-fns']
    },
    optimizeDeps: {
      include: ['lucide-svelte', 'date-fns', 'date-fns/locale'],
      // Svelte 5 a veces requiere excluirse de la pre-optimización para evitar conflictos de versiones
      exclude: ['svelte'] 
    },
    plugins: [
      tailwindcss()
    ],
    server: {
      // Mantenemos false para velocidad en Linux, como indica tu estructura
      watch: {
        usePolling: false, 
      }
    }
  }
});