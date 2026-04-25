import { api, API_ROUTES } from '@/config/api';

/**
 * Servicio para la gestión de departamentos.
 * Alineado con la estructura de FastAPI: /api/v1/department/
 */
export const departmentService = {
  // 1. Obtener todos (GET /api/v1/department/)
  // Importante: Incluimos la "/" final que exige FastAPI
  getAll: () =>
    api.request(`${API_ROUTES.DEPARTMENT.BASE}/`),

  // 2. Crear uno nuevo (POST /api/v1/department/)
  create: (data: { name: string; description: string; is_active?: boolean }) =>
    api.request(`${API_ROUTES.DEPARTMENT.BASE}/`, 'POST', data),

  // 3. Obtener por ID (GET /api/v1/department/{id})
  getById: (id: number | string) =>
    api.request(`${API_ROUTES.DEPARTMENT.BASE}/${id}`),

  // 4. Actualizar (PUT /api/v1/department/{id})
  update: (id: number | string, data: any) =>
    api.request(`${API_ROUTES.DEPARTMENT.BASE}/${id}`, 'PUT', data),

  // 5. Borrado físico (DELETE /api/v1/department/{id})
  delete: (id: number | string) =>
    api.request(`${API_ROUTES.DEPARTMENT.BASE}/${id}`, 'DELETE'),
};