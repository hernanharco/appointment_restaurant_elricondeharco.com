// API service for restaurant reservation system
const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
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

  // Reservations
  async getReservations(date = null) {
    const params = date ? `?date=${date}` : '';
    return this.request(`/reservations/${params}`);
  }

  async getReservation(id) {
    return this.request(`/reservations/${id}`);
  }

  async createReservation(reservationData) {
    return this.request('/reservations/', {
      method: 'POST',
      body: JSON.stringify(reservationData),
    });
  }

  async updateReservation(id, reservationData) {
    return this.request(`/reservations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(reservationData),
    });
  }

  async cancelReservation(id) {
    return this.request(`/reservations/${id}`, {
      method: 'DELETE',
    });
  }

  async confirmReservation(id) {
    return this.request(`/reservations/${id}/confirm`, {
      method: 'POST',
    });
  }

  async getReservationsByPhone(phone) {
    return this.request(`/reservations/client/phone/${phone}`);
  }

  async getDailySummary(date) {
    return this.request(`/reservations/daily-summary/${date}`);
  }

  // Availability
  async getAvailability(date, partySize) {
    return this.request(`/availability/?date=${date}&party_size=${partySize}`);
  }

  // Clients
  async getClients() {
    return this.request('/clients/');
  }

  async createClient(clientData) {
    return this.request('/clients/', {
      method: 'POST',
      body: JSON.stringify(clientData),
    });
  }

  async getClientByPhone(phone) {
    return this.request(`/clients/search/${phone}`);
  }

  async updateClient(id, clientData) {
    return this.request(`/clients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clientData),
    });
  }

  // Business Hours
  async getBusinessHours() {
    return this.request('/business-hours/');
  }

  // Health check
  async healthCheck() {
    return this.request('/health', { baseURL: 'http://localhost:8000' });
  }
}

export const apiService = new ApiService();
export default apiService;
