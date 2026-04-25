import { api, API_ROUTES } from '@/config/api';

/**
 * API para la gestión de disponibilidad y huecos libres.
 */
export const availabilityApi = {
  /**
   * Obtener slots (huecos) disponibles.
   * [cite: 2026-02-07]
   */
  getSlots: (date: string, serviceId: number, collaboratorId?: number | null) => {
    const params = new URLSearchParams({
      date,
      service_id: serviceId.toString(),
    });

    // Solo añadimos el colaborador si existe [cite: 2026-01-30]
    if (collaboratorId) {
      params.append('collaborator_id', collaboratorId.toString());
    }

    return api.request(`${API_ROUTES.AVAILABILITY.BASE}?${params.toString()}`);
  },

  /**
   * Obtener configuración de un día específico.
   */
  getDayConfig: (dayName: string, collaboratorId: number) => {
    const params = new URLSearchParams({
      collaborator_id: collaboratorId.toString(),
    });
    return api.request(`${API_ROUTES.BUSINESS_HOURS}/day/${dayName}?${params.toString()}`);
  }
};