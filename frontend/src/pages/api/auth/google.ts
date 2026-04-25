// src/pages/api/auth/google.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request, cookies }) => {
  const AUTH_API_URL = import.meta.env.PUBLIC_AUTH_API_URL;
  const body = await request.json();

  const response = await fetch(`${AUTH_API_URL}/api/v1/auth/google`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (response.ok) {
    const setCookie = response.headers.get('set-cookie');
    if (setCookie) {
      const tokenMatch = setCookie.match(/access_token=([^;]+)/);
      if (tokenMatch?.[1]) {  // ✅ corrige el error de undefined
        const isProd = import.meta.env.MODE === 'production';
        cookies.set('access_token', tokenMatch[1], {
          httpOnly: true,
          secure: isProd,
          sameSite: isProd ? 'none' : 'lax',
          maxAge: 60 * 60 * 24,
          path: '/',
        });
      }
    }
  }

  return new Response(JSON.stringify(data), {
    status: response.status,
    headers: { 'Content-Type': 'application/json' },
  });
};