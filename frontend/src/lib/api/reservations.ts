/**
 * reservations.ts
 * API client para reservas de restaurante
 */
import type { 
    Reservation, 
    CreateReservationDTO, 
    RestaurantAvailabilityResponse,
    RestaurantConfig 
} from '@/types/reservations';

const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

class ReservationsAPI {
    private async request<T>(
        endpoint: string, 
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${API_BASE}${endpoint}`;
        
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        return response.json();
    }

    // --- Configuración del restaurante ---
    async getRestaurantConfig(): Promise<RestaurantConfig> {
        return this.request<RestaurantConfig>('/api/restaurant-config');
    }

    // --- Disponibilidad ---
    async getAvailability(params: {
        date: string;
        party_size: number;
    }): Promise<RestaurantAvailabilityResponse> {
        const searchParams = new URLSearchParams({
            date: params.date,
            party_size: params.party_size.toString(),
        });
        
        return this.request<RestaurantAvailabilityResponse>(
            `/api/reservations/availability?${searchParams}`
        );
    }

    // --- CRUD de Reservas ---
    async create(data: CreateReservationDTO): Promise<Reservation> {
        return this.request<Reservation>('/api/reservations', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async get(id: number): Promise<Reservation> {
        return this.request<Reservation>(`/api/reservations/${id}`);
    }

    async getAll(params?: {
        date?: string;
        client_phone?: string;
        limit?: number;
        offset?: number;
    }): Promise<Reservation[]> {
        const searchParams = new URLSearchParams();
        
        if (params?.date) searchParams.append('date', params.date);
        if (params?.client_phone) searchParams.append('client_phone', params.client_phone);
        if (params?.limit) searchParams.append('limit', params.limit.toString());
        if (params?.offset) searchParams.append('offset', params.offset.toString());

        const queryString = searchParams.toString();
        return this.request<Reservation[]>(
            `/api/reservations${queryString ? `?${queryString}` : ''}`
        );
    }

    async update(id: number, data: Partial<CreateReservationDTO>): Promise<Reservation> {
        return this.request<Reservation>(`/api/reservations/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    async delete(id: number): Promise<void> {
        await this.request<void>(`/api/reservations/${id}`, {
            method: 'DELETE',
        });
    }

    // --- Acciones de negocio ---
    async confirm(id: number): Promise<Reservation> {
        return this.request<Reservation>(`/api/reservations/${id}/confirm`, {
            method: 'POST',
        });
    }

    async cancel(id: number): Promise<Reservation> {
        return this.request<Reservation>(`/api/reservations/${id}/cancel`, {
            method: 'POST',
        });
    }

    // --- Estadísticas ---
    async getDailyCapacity(date: string): Promise<{
        date: string;
        max_capacity: number;
        total_reservations: number;
        total_people: number;
        hourly_occupancy: Record<number, number>;
        peak_hour: number | null;
    }> {
        return this.request(`/api/reservations/capacity/${date}`);
    }

    async getClientReservations(clientId: number): Promise<Reservation[]> {
        return this.request<Reservation[]>(`/api/reservations/client/${clientId}`);
    }
}

// Exportamos una instancia singleton
export const reservationsApi = new ReservationsAPI();
