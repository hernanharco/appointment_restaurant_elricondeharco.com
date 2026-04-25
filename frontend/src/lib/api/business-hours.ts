import { api, API_ROUTES } from '@/config/api';
import { DAYS_LABELS } from '@/lib/constants/days';

export const businessHoursApi = {
  /**
   * Obtiene la configuración semanal completa de un colaborador.
   */
  getWeeklyConfig: (collaboratorId: string | number) => {
    const url = `${API_ROUTES.BUSINESS_HOURS.BASE}/?collaborator_id=${collaboratorId}`;
    return api.request(url);
  },

  /**
   * 🚀 GUARDADO MASIVO (Bulk Update)
   * Envía toda la semana en una sola transacción.
   * @param collaboratorId ID del colaborador
   * @param config Objeto del store mapeado al Schema BulkBusinessHoursUpdate
   */
  updateBulkConfig: async (collaboratorId: number, config: any) => {
    // Transformamos el objeto config {1: {...}, 2: {...}} en una lista para Pydantic
    const schedules = DAYS_LABELS.map(day => {
      const dayData = config[day.id] || {
        day_of_week: day.id,
        day_name: day.name,
        is_enabled: false,
        time_slots: []
      };

      return {
        day_of_week: day.id,
        day_name: day.name,
        is_enabled: dayData.is_enabled,
        is_split_shift: dayData.is_split_shift || false,
        time_slots: dayData.time_slots || []
      };
    });

    const payload = {
      collaborator_id: collaboratorId,
      schedules: schedules
    };

    return api.request(API_ROUTES.BUSINESS_HOURS.BULK_UPDATE, 'POST', payload);
  },

  /**
   * Obtiene el rango de apertura GLOBAL del local.
   */
  getGlobalRange: (dayOfWeek: number) => {
    const url = `${API_ROUTES.BUSINESS_HOURS.BASE}/global-range?day_of_week=${dayOfWeek}`;
    return api.request(url);
  },

  /**
   * Elimina toda la configuración de un colaborador (limpieza total).
   */
  deleteByCollaborator: (collaboratorId: number) => {
    return api.request(`${API_ROUTES.BUSINESS_HOURS.BASE}/collaborator/${collaboratorId}`, 'DELETE');
  }
};