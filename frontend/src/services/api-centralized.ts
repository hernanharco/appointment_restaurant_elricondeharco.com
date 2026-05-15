/**
 * API Centralizada para CoreAppointment
 * Maneja toda la comunicación con el backend desde un solo lugar
 * Usa las variables de entorno del .env — sin puertos hardcodeados.
 */

const BASE_URL      = import.meta.env.PUBLIC_API_BACKEND ?? 'http://localhost:8003';
const V1            = import.meta.env.PUBLIC_API_VERSION ?? '/api/v1';
const API_BASE_URL  = `${BASE_URL}${V1}`;


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
   * Usa la misma BASE_URL que el resto de la clase (desde .env)
   */
  async healthCheck(): Promise<any> {
    const response = await fetch(`${BASE_URL}/health`);

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

  // --- Horarios del Restaurante ---

  async getRestaurantHours(): Promise<any> {
    return this.request<any>('/restaurant-hours/');
  }

  async updateRestaurantHours(hoursData: { days: any[] }): Promise<any> {
    return this.request<any>('/restaurant-hours/', {
      method: 'PUT',
      body: JSON.stringify(hoursData),
    });
  }

  // --- Historial y Exportación ---

  async getHistory(params: {
    page?: number; per_page?: number;
    start_date?: string; end_date?: string;
    status?: string; search?: string;
  } = {}): Promise<any> {
    const q = new URLSearchParams();
    if (params.page) q.set('page', String(params.page));
    if (params.per_page) q.set('per_page', String(params.per_page));
    if (params.start_date) q.set('start_date', params.start_date);
    if (params.end_date) q.set('end_date', params.end_date);
    if (params.status) q.set('status', params.status);
    if (params.search) q.set('search', params.search);
    return this.request<any>(`/reservations/history?${q.toString()}`);
  }

  async getStats(params: {
    start_date?: string; end_date?: string;
  } = {}): Promise<any> {
    const q = new URLSearchParams();
    if (params.start_date) q.set('start_date', params.start_date);
    if (params.end_date) q.set('end_date', params.end_date);
    return this.request<any>(`/reservations/stats?${q.toString()}`);
  }

  getExportCsvUrl(params: {
    start_date?: string; end_date?: string; status?: string;
  } = {}): string {
    const q = new URLSearchParams();
    if (params.start_date) q.set('start_date', params.start_date);
    if (params.end_date) q.set('end_date', params.end_date);
    if (params.status) q.set('status', params.status);
    return `${this.baseURL}/reservations/export/csv?${q.toString()}`;
  }

  getExportExcelUrl(params: {
    start_date?: string; end_date?: string; status?: string;
  } = {}): string {
    const q = new URLSearchParams();
    if (params.start_date) q.set('start_date', params.start_date);
    if (params.end_date) q.set('end_date', params.end_date);
    if (params.status) q.set('status', params.status);
    return `${this.baseURL}/reservations/export/excel?${q.toString()}`;
  }
}

// Exportamos una instancia singleton
export const apiCentralized = new ApiCentralized();
export default apiCentralized;

// Exportamos tipos para usar en los componentes
export type { ReservationData, ClientData, AvailabilityRequest };
