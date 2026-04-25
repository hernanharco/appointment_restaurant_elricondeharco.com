import { api, API_ROUTES } from '../../config/api';
import type { Client, CreateClientInput, UpdateClientInput } from '@/types/clients';

/**
 * CLIENTS API SERVICE
 * Encargado de la comunicación con FastAPI para el dominio de Clientes.
 */
export const clientsApi = {
  /**
   * Busca un cliente por teléfono. 
   * Retorna null si no existe (404) para facilitar lógica de "Nuevo Cliente".
   */
  searchByPhone: async (phone: string): Promise<Client | null> => {
    try {
      return await api.request(`${API_ROUTES.CLIENTS.SEARCH}/${phone}`);
    } catch (error: any) {
      // Si el backend lanza 404, el cliente es nuevo para el sistema
      if (error.message?.includes('404')) {
        return null;
      }
      throw error;
    }
  },

  /**
   * Obtiene la lista completa de clientes.
   */
  getAll: (): Promise<Client[]> => {
    return api.request(`${API_ROUTES.CLIENTS.BASE}/`);
  },

  /**
   * Registra un nuevo cliente en el sistema.
   */
  create: (data: CreateClientInput): Promise<Client> => {
    // Correcto: (endpoint, método, datos)
    return api.request(API_ROUTES.CLIENTS.BASE, 'POST', data);
  },

  /**
   * Actualiza los datos de un cliente existente.
   */
  update: (id: number, data: UpdateClientInput): Promise<Client> => {
    return api.request(`${API_ROUTES.CLIENTS.BASE}/${id}`, 'PUT', data);
  },

  /**
   * Elimina un cliente (o lo desactiva según la lógica de tu backend).
   */
  delete: (id: number): Promise<{ ok: boolean }> => {
    return api.request(`${API_ROUTES.CLIENTS.BASE}/${id}`, 'DELETE');
  }


};