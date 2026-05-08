/**
 * reservation-state.svelte.ts
 * Store para gestionar el estado de las reservas en el frontend
 */
import type { Reservation } from '@/types/reservations';

class ReservationStateStore {
    // Estado del modal
    isModalOpen = $state(false);
    dateForNewReservation = $state('');
    
    // Lista de reservas
    items = $state<Reservation[]>([]);
    isLoading = $state(false);
    error = $state<string | null>(null);

    // Fecha seleccionada globalmente
    selectedDate = $state(new Date());

    // Métodos del modal
    openModal(date?: string) {
        this.isModalOpen = true;
        this.dateForNewReservation = date || this.selectedDate.toISOString().split('T')[0];
    }

    closeModal() {
        this.isModalOpen = false;
        this.dateForNewReservation = '';
    }

    // Método para cambiar la fecha
    setSelectedDate(date: Date) {
        this.selectedDate = date;
    }

    // Métodos de gestión de reservas
    async refresh() {
        this.isLoading = true;
        this.error = null;
        
        try {
            // Aquí iría la llamada a la API para obtener reservas
            // Por ahora simulamos con un array vacío
            this.items = [];
        } catch (err) {
            this.error = err instanceof Error ? err.message : 'Error loading reservations';
        } finally {
            this.isLoading = false;
        }
    }

    // Método para obtener reservas por fecha
    getReservationsByDate(date: string): Reservation[] {
        return this.items.filter(reservation => {
            const reservationDate = new Date(reservation.start_time).toISOString().split('T')[0];
            return reservationDate === date;
        });
    }
}

// Exportamos una instancia singleton
export const reservationStore = new ReservationStateStore();
