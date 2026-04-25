// src/pages/api/auth/logout.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ cookies }) => {
  const AUTH_API_URL = import.meta.env.PUBLIC_AUTH_API_URL;

  await fetch(`${AUTH_API_URL}/api/v1/auth/logout`, {
    method: 'POST',
  });

  // ✅ Borrar cookie en Astro
  cookies.delete('access_token', { path: '/' });

  return new Response(JSON.stringify({ message: 'Sesión cerrada' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};