/**
 * NÚCLEO DE COMUNICACIÓN API
 * Toda configuración viene del .env — sin datos estáticos en el código.
 * Proyecto Appointment
 */

const BASE_URL      = import.meta.env.PUBLIC_API_BACKEND;
const AUTH_BASE_URL = import.meta.env.PUBLIC_AUTH_API_URL;
const V1            = import.meta.env.PUBLIC_API_VERSION ?? '/api/v1';  // ✅ desde .env

export const API_ROUTES = {
  DEPARTMENT:     { BASE: `${V1}/department` },
  COLLABORATORS:  { BASE: `${V1}/collaborators`, STATS: `${V1}/collaborators/stats` },
  SERVICES:       { BASE: `${V1}/services`, STATS: `${V1}/services/stats` },
  CLIENTS:        { BASE: `${V1}/clients`, SEARCH: `${V1}/clients/search` },
  APPOINTMENTS: {
    BASE:         `${V1}/appointments`,
    STATS:        `${V1}/appointments/stats`,
    AVAILABILITY: `${V1}/appointments/availability`,
    SUMMARY:      `${V1}/appointments/summary`,
    COUNT_BY_DAY: `${V1}/appointments/count-by-day`,
  },
  AVAILABILITY:   { BASE: `${V1}/availability` },
  BUSINESS_HOURS: {
    BASE:         `${V1}/business-hours`,
    BULK_UPDATE:  `${V1}/business-hours/bulk-update`,
    GLOBAL_RANGE: `${V1}/business-hours/global-range`,
  },
  NOTIFICATIONS:  { STREAM: `${V1}/notifications/stream` },
  HEALTH:         { STATUS: `/health` },

  AUTH: {
    GOOGLE: `${V1}/auth/google`,
    LOGOUT: `${V1}/auth/logout`,
    ME:     `${V1}/users/me`,
    LOGIN_FORM: `${V1}/auth/login-form`, 
    PENDING:    '/pending',
  },
};

/**
 * Helper interno para construir y ejecutar requests
 */
async function makeRequest(baseUrl: string, endpoint: string, method = 'GET', body?: any) {
  const config: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  };
  if (body) config.body = JSON.stringify(body);

  const response = await fetch(`${baseUrl}${endpoint}`, config);
  if (response.status === 204) return {};

  const text = await response.text();
  const data = text ? JSON.parse(text) : {};

  if (!response.ok) {
    throw new Error(data.detail || `Error ${response.status}: ${response.statusText}`);
  }

  return data;
}

/**
 * UTILIDAD DE PETICIONES — backend principal (PUBLIC_API_BACKEND)
 */
export const api = {
  async request(endpoint: string, method = 'GET', body?: any) {
    try {
      return await makeRequest(BASE_URL, endpoint, method, body);
    } catch (err) {
      console.error('❌ API Error:', err);
      throw err;
    }
  }
};

/**
 * UTILIDAD DE PETICIONES — backend de autenticación (PUBLIC_AUTH_API_URL)
 */
export const authApi = {
  async request(endpoint: string, method = 'GET', body?: any) {
    try {
      return await makeRequest(AUTH_BASE_URL, endpoint, method, body);
    } catch (err) {
      console.error('❌ Auth API Error:', err);
      throw err;
    }
  }
};