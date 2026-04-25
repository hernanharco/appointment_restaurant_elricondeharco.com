// src/lib/api/auth.ts
import { API_ROUTES } from '@/config/api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: 'SUPERADMIN' | 'ADMIN' | 'MANAGER' | 'USER' | 'VIEWER' | 'NONE';
  status: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED' | 'PENDING';
  is_active: boolean;
  last_login?: string | null;
  created_at: string;
  updated_at: string;
}

export class AuthApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = 'AuthApiError';
  }
}

export async function loginUser(credentials: LoginCredentials): Promise<LoginResponse> {
  // FastAPI OAuth2 espera form-data con username/password
  const formData = new URLSearchParams();
  formData.append('username', credentials.email);
  formData.append('password', credentials.password);

  const AUTH_API_URL = import.meta.env.PUBLIC_AUTH_API_URL;

  const response = await fetch(`${AUTH_API_URL}${API_ROUTES.AUTH.LOGIN_FORM}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString(),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error de autenticación' }));
    throw new AuthApiError(response.status, error.detail || 'Credenciales incorrectas');
  }

  return response.json();
}

export async function fetchCurrentUser(token: string): Promise<UserProfile> {
  const AUTH_API_URL = import.meta.env.PUBLIC_AUTH_API_URL;

  const response = await fetch(`${AUTH_API_URL}${API_ROUTES.AUTH.ME}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new AuthApiError(response.status, 'Sesión expirada');
  }

  return response.json();
}

export async function verifyToken(token: string): Promise<boolean> {
  try {
    await fetchCurrentUser(token);
    return true;
  } catch {
    return false;
  }
}