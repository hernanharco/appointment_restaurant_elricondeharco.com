import { api, API_ROUTES } from '@/config/api';

/**
 * API para el monitoreo del sistema (Health Check).
 * Permite verificar si el backend y la base de datos están operativos.
 */
export const healthApi = {
  /**
   * Verifica el estado de salud general del backend.
   * GET /api/v1/health
   */
  checkStatus: () =>
    api.request(API_ROUTES.HEALTH.STATUS, 'GET'),

  /**
   * Opcional: Podrías tener un ping más ligero si el backend lo soporta.
   */
  ping: () =>
    api.request(`${API_ROUTES.HEALTH.STATUS}/ping`, 'GET').catch(() => ({ status: 'down' }))
};