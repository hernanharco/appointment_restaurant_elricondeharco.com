/**
 * src/types/reservations.ts
 * Responsabilidad: Definiciones de tipos para el dominio de reservas de restaurante.
 * Reemplaza la lógica de appointments por capacity-based reservations.
 */

export type ReservationStatus = 'scheduled' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled' | 'no_show';

/**
 * 🏢 INTERFAZ: RestaurantConfig
 * Configuración del restaurante para capacidad y horarios
 */
export interface RestaurantConfig {
    id: number;
    name: string;
    max_capacity: number;
    time_slot_duration_minutes: number;
    max_party_size: number;
    min_party_size: number;
    is_active: boolean;
}

/**
 * 🕒 INTERFAZ: AvailableTimeSlot
 * Slot de tiempo disponible basado en capacidad del restaurante
 */
export interface AvailableTimeSlot {
    start_time: string;
    end_time: string;
    available_capacity: number;
    total_capacity: number;
}

/**
 * 📦 INTERFAZ PRINCIPAL: Reservation
 * Refleja el modelo de SQLAlchemy para reservas de restaurante
 */
export interface Reservation {
    id?: number;
    client_id: number | null;
    client_name: string;
    client_phone: string | null;
    client_email: string | null;
    client_notes: string | null;
    
    // --- CAMPO CLAVE: party_size ---
    party_size: number;
    
    start_time: string; // ISO String desde el Backend
    end_time: string;   // ISO String desde el Backend
    
    status: ReservationStatus;
    source: string;
    created_at?: string;
    updated_at?: string;
}

/**
 * 📦 DTO: CreateReservationDTO
 * Lo que enviamos al endpoint POST /reservations/
 */
export interface CreateReservationDTO {
    client_id: number | null;
    client_name: string;
    client_phone: string;
    client_email?: string | null;
    client_notes?: string | null;
    party_size: number;
    start_time: string; 
    end_time: string;   
    status: ReservationStatus;
    source?: string; 
}

/**
 * 📊 INTERFAZ: RestaurantAvailabilityResponse
 * Respuesta completa de disponibilidad del restaurante
 */
export interface RestaurantAvailabilityResponse {
    date: string;
    party_size: number;
    available_slots: AvailableTimeSlot[];
    total_slots: number;
    restaurant_config: RestaurantConfig;
}

/**
 * 📊 INTERFAZ: DayCountResponse
 * Para las respuestas de estadísticas del carrusel (mantenemos compatibilidad)
 */
export interface DayCountResponse {
    date: string;
    count: number;
}

/**
 * 🎯 INTERFAZ: ReservationFormData
 * Estado del formulario de reserva en el frontend
 */
export interface ReservationFormData {
    // --- Datos del cliente ---
    client_id: number | null;
    client_name: string;
    client_phone: string;
    client_email: string;
    client_notes: string;
    
    // --- Datos de la reserva ---
    party_size: number;
    date: string;
    time: string;
    
    // --- Metadatos ---
    duration_minutes: number;
    id?: number; // Para modo edición
}
