// Proyecto Appointment

import { defineMiddleware } from 'astro:middleware';
import { API_ROUTES } from '@/config/api';

const PUBLIC_ROUTES   = ['/login', '/pending'];
const PUBLIC_PREFIXES = ['/_astro/', '/assets/', '/fonts/', '/favicon', '/api/auth/'];

const ALLOWED_ROLES = ['SUPERADMIN', 'ADMIN', 'MANAGER'];

export const onRequest = defineMiddleware(async (context, next) => {
  const { url, cookies, redirect } = context;
  const pathname = new URL(url).pathname;

  console.log('🔍 pathname:', pathname);  // 👇

  const isPublicPrefix = PUBLIC_PREFIXES.some((p) => pathname.startsWith(p));
  const isPublicRoute  = PUBLIC_ROUTES.includes(pathname);

  console.log('isPublicRoute:', isPublicRoute, '| isPublicPrefix:', isPublicPrefix);  // 👇

  if (isPublicPrefix || isPublicRoute) return next();

  const token = cookies.get('access_token')?.value;
  console.log('token existe:', !!token);  // 👇

  if (!token) {
    const loginUrl = new URL('/login', url);
    loginUrl.searchParams.set('redirect', pathname);
    return redirect(loginUrl.toString());
  }

  try {
    const AUTH_API_URL = import.meta.env.PUBLIC_AUTH_API_URL;
    console.log('AUTH_API_URL:', AUTH_API_URL);  // 👇
    console.log('ROUTE_ME:', API_ROUTES.AUTH.ME);  // 👇

    const response = await fetch(`${AUTH_API_URL}${API_ROUTES.AUTH.ME}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('response.status:', response.status);  // 👇

    if (!response.ok) {
      cookies.delete('access_token', { path: '/' });
      const loginUrl = new URL('/login', url);
      loginUrl.searchParams.set('redirect', pathname);
      return redirect(loginUrl.toString());
    }

    const user = await response.json();
    const role   = user.role?.toUpperCase();
    const status = user.status?.toUpperCase();

    console.log('role:', role, '| status:', status, '| is_active:', user.is_active);
    console.log('ALLOWED?', ALLOWED_ROLES.includes(role));

    if (role === 'NONE' || status !== 'ACTIVE' || !user.is_active) {
      console.log('❌ Bloqueado por role/status/is_active');
      return redirect('/pending');
    }

    if (!ALLOWED_ROLES.includes(role)) {
      console.log('❌ Bloqueado por rol no permitido:', role);
      return redirect('/pending');
    }

    console.log('✅ Acceso permitido');
    context.locals.user = user;
    return next();

  } catch (err) {
    console.log('❌ Error en middleware:', err);  // 👇 capturar el error real
    cookies.delete('access_token', { path: '/' });
    return redirect('/login');
  }
});