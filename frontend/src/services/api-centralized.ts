/**
 * API Centralizada para CoreAppointment
 * Maneja toda la comunicación con el backend desde un solo lugar
 */

const API_BASE_URL = 'http://localhost:8003/api/v1';


interface ReservationData {
  client_name: string;
  client_phone: string;
  client_email?: string;
  client_notes?: string;
  party_size: number;
  start_time: string;
  end_time: string;
}

interface ClientData {
  name: string;
  phone: string;
  email?: string;
  notes?: string;
}

interface AvailabilityRequest {
  date: string;
  party_size: number;
}

class ApiCentralized {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // ===== RESERVAS =====

  /**
   * Obtener reservas por fecha
   */
  async getReservationsByDate(date: string): Promise<any[]> {
    return this.request<any[]>(`/reservations/?date=${date}`);
  }

  /**
   * Crear nueva reserva
   */
  async createReservation(reservationData: ReservationData): Promise<any> {
    return this.request<any>('/reservations/', {
      method: 'POST',
      body: JSON.stringify(reservationData),
    });
  }

  /**
   * Actualizar reserva existente
   */
  async updateReservation(id: number, reservationData: Partial<ReservationData>): Promise<any> {
    return this.request<any>(`/reservations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(reservationData),
    });
  }

  /**
   * Cancelar reserva
   */
  async cancelReservation(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/reservations/${id}`, {
      method: 'DELETE',
    });
  }

  /**
   * Confirmar reserva
   */
  async confirmReservation(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/reservations/${id}/confirm`, {
      method: 'POST',
    });
  }

  /**
   * Obtener reservas por teléfono de cliente
   */
  async getReservationsByPhone(phone: string): Promise<any[]> {
    return this.request<any[]>(`/reservations/client/phone/${phone}`);
  }

  /**
   * Obtener resumen diario
   */
  async getDailySummary(date: string): Promise<any> {
    return this.request<any>(`/reservations/daily-summary/${date}`);
  }

  // ===== CLIENTES =====

  /**
   * Crear nuevo cliente
   */
  async createClient(clientData: ClientData): Promise<any> {
    return this.request<any>('/clients/', {
      method: 'POST',
      body: JSON.stringify(clientData),
    });
  }

  /**
   * Obtener lista de clientes
   */
  async getClients(skip = 0, limit = 100): Promise<any[]> {
    return this.request<any[]>(`/clients/?skip=${skip}&limit=${limit}`);
  }

  /**
   * Buscar cliente por teléfono
   */
  async getClientByPhone(phone: string): Promise<any> {
    return this.request<any>(`/clients/search/${phone}`);
  }

  /**
   * Actualizar cliente
   */
  async updateClient(id: number, clientData: Partial<ClientData>): Promise<any> {
    return this.request<any>(`/clients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clientData),
    });
  }

  // ===== DISPONIBILIDAD =====

  /**
   * Ver disponibilidad para una fecha y tamaño de grupo
   */
  async getAvailability(date: string, partySize: number): Promise<any> {
    const params = new URLSearchParams({
      date,
      party_size: partySize.toString()
    });
    return this.request<any>(`/availability/?${params}`);
  }

  // ===== HORARIOS DE NEGOCIO =====

  /**
   * Obtener horarios de negocio
   */
  async getBusinessHours(collaboratorId: number): Promise<any[]> {
    return this.request<any[]>(`/business-hours/?collaborator_id=${collaboratorId}`);
  }

  /**
   * Actualizar horarios de negocio (bulk update)
   */
  async updateBusinessHours(collaboratorId: number, schedules: any[]): Promise<any> {
    return this.request<any>('/business-hours/bulk-update', {
      method: 'POST',
      body: JSON.stringify({
        collaborator_id: collaboratorId,
        schedules
      }),
    });
  }

  // ===== HEALTH CHECK =====

  /**
   * Verificar salud del API
   */
  async healthCheck(): Promise<any> {
    const url = 'http://localhost:8000/health';
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return await response.json();
  }

  // ===== RESTAURANT CONFIG =====

  /**
   * Obtener configuración activa del restaurante
   */
  async getActiveRestaurantConfig(): Promise<any> {
    return this.request<any>('/restaurant-config/active');
  }

  /**
   * Crear nueva configuración del restaurante
   */
  async createRestaurantConfig(configData: any): Promise<any> {
    return this.request<any>('/restaurant-config/', {
      method: 'POST',
      body: JSON.stringify(configData),
    });
  }

  /**
   * Actualizar configuración del restaurante
   */
  async updateRestaurantConfig(id: number, configData: any): Promise<any> {
    return this.request<any>(`/restaurant-config/${id}`, {
      method: 'PUT',
      body: JSON.stringify(configData),
    });
  }

  /**
   * Obtener todas las configuraciones del restaurante
   */
  async getAllRestaurantConfigs(): Promise<any[]> {
    return this.request<any[]>('/restaurant-config/');
  }
}

// Exportamos una instancia singleton
export const apiCentralized = new ApiCentralized();
export default apiCentralized;

// Exportamos tipos para usar en los componentes
export type { ReservationData, ClientData, AvailabilityRequest };
