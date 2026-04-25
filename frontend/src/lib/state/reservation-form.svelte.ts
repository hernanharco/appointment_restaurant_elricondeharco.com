/**
 * reservation-form.svelte.ts
 * Store para gestión de reservas con Svelte 5 Runes
 */
import { reservationStore } from '../stores/reservation-state.svelte';
import { reservationsApi } from '@/lib/api/reservations';
import { clientStore } from './client-state.svelte';
import { toastStore } from './toast-state.svelte';
import { format } from 'date-fns';
import type { 
    AvailableTimeSlot, 
    CreateReservationDTO, 
    ReservationStatus, 
    Reservation,
    RestaurantConfig
} from '@/types/reservations';

class ReservationFormManager {
    // Estado reactivo
    formData = $state({
        id: undefined as number | undefined,
        client_id: undefined as number | undefined,
        client_name: '',
        client_phone: '',
        client_email: '',
        client_notes: '',
        party_size: 2,
        date: '',
        time: '',
        duration_minutes: 60,
    });

    restaurantConfig = $state<RestaurantConfig | null>(null);
    slots = $state<AvailableTimeSlot[]>([]);
    isLoadingSlots = $state(false);
    isSaving = $state(false);
    saveSuccess = $state(false);

    // Estados derivados
    private readonly isValidForm = $derived(
        this.formData.client_name.trim() !== '' &&
        this.formData.client_phone.trim() !== '' &&
        this.formData.party_size > 0 &&
        this.formData.date !== '' &&
        this.formData.time !== ''
    );

    private readonly canFetchSlots = $derived(
        this.formData.date !== '' && 
        this.formData.party_size > 0 &&
        this.restaurantConfig !== null
    );

    // Effects
    $effect(() => {
        if (this.canFetchSlots && !this.isLoadingSlots) {
            this.fetchAvailableSlots();
        }
    });

    $effect(() => {
        if (this.formData.party_size || this.formData.date) {
            this.formData.time = '';
        }
    });

    // Métodos
    async loadRestaurantConfig(): Promise<void> {
        try {
            const config = await reservationsApi.getRestaurantConfig();
            this.restaurantConfig = config;
        } catch (error) {
            console.error('Error loading restaurant config:', error);
            toastStore.show('No se pudo cargar la configuración del restaurante', 'error');
        }
    }

    loadReservation(reservation: Reservation): void {
        this.resetForm();
        const start = new Date(reservation.start_time);
        
        this.formData = {
            id: Number(reservation.id),
            client_id: reservation.client_id || undefined,
            client_name: reservation.client_name,
            client_phone: reservation.client_phone || '',
            client_email: reservation.client_email || '',
            client_notes: reservation.client_notes || '',
            party_size: reservation.party_size,
            date: format(start, 'yyyy-MM-dd'),
            time: format(start, 'HH:mm'),
            duration_minutes: 60,
        };
    }

    resetForm(): void {
        this.formData = {
            id: undefined,
            client_id: undefined,
            client_name: '',
            client_phone: '',
            client_email: '',
            client_notes: '',
            party_size: 2,
            date: '',
            time: '',
            duration_minutes: 60,
        };
        this.slots = [];
        this.saveSuccess = false;
    }

    async fetchAvailableSlots(): Promise<void> {
        if (!this.formData.date || !this.formData.party_size || !this.restaurantConfig) {
            return;
        }

        this.isLoadingSlots = true;
        this.slots = [];

        try {
            const response = await reservationsApi.getAvailability({
                date: this.formData.date,
                party_size: this.formData.party_size,
            });

            this.slots = response.available_slots;
        } catch (error) {
            console.error('Error fetching available slots:', error);
            toastStore.show('No se pudo cargar la disponibilidad. Intenta de nuevo.', 'error');
            this.slots = [];
        } finally {
            this.isLoadingSlots = false;
        }
    }

    selectSlot(slot: AvailableTimeSlot): void {
        const startTime = new Date(slot.start_time);
        this.formData.time = format(startTime, 'HH:mm');
        
        const endTime = new Date(slot.end_time);
        const duration = Math.round((endTime.getTime() - startTime.getTime()) / (1000 * 60));
        this.formData.duration_minutes = duration;
    }

    async handlePhoneInput(): Promise<void> {
        const phone = this.formData.client_phone.trim();
        if (phone.length >= 9) {
            try {
                const client = await clientStore.findByPhone(phone);
                if (client) {
                    this.formData.client_id = client.id;
                    this.formData.client_name = client.full_name;
                    this.formData.client_email = client.email || '';
                    toastStore.show('✅ Cliente reconocido', 'success');
                } else {
                    this.formData.client_id = undefined;
                }
            } catch (error) {
                console.error('Error searching client:', error);
            }
        } else {
            this.formData.client_id = undefined;
        }
    }

    async save(): Promise<void> {
        if (!this.isValidForm) {
            toastStore.show('Por favor, completa todos los campos requeridos', 'error');
            return;
        }

        if (this.restaurantConfig) {
            if (this.formData.party_size < this.restaurantConfig.min_party_size) {
                toastStore.show(`El tamaño mínimo de grupo es ${this.restaurantConfig.min_party_size} personas`, 'error');
                return;
            }
            if (this.formData.party_size > this.restaurantConfig.max_party_size) {
                toastStore.show(`El tamaño máximo de grupo es ${this.restaurantConfig.max_party_size} personas`, 'error');
                return;
            }
        }

        this.isSaving = true;
        this.saveSuccess = false;

        try {
            const startDateTime = new Date(`${this.formData.date}T${this.formData.time}:00`);
            const endDateTime = new Date(startDateTime.getTime() + this.formData.duration_minutes * 60000);

            const reservationData: CreateReservationDTO = {
                client_id: this.formData.client_id,
                client_name: this.formData.client_name,
                client_phone: this.formData.client_phone,
                client_email: this.formData.client_email,
                client_notes: this.formData.client_notes,
                party_size: this.formData.party_size,
                start_time: startDateTime.toISOString(),
                end_time: endDateTime.toISOString(),
                status: 'scheduled' as ReservationStatus,
                source: 'web',
            };

            if (this.formData.id) {
                await reservationsApi.update(this.formData.id, reservationData);
                toastStore.show('✅ Reserva actualizada correctamente', 'success');
            } else {
                await reservationsApi.create(reservationData);
                toastStore.show('🎉 ¡Reserva confirmada!', 'success');
            }

            this.saveSuccess = true;
            await reservationStore.refresh();

        } catch (error: any) {
            console.error('Error saving reservation:', error);
            const message = error.response?.data?.detail || 'Error al guardar la reserva';
            toastStore.show(message, 'error');
            this.saveSuccess = false;
        } finally {
            this.isSaving = false;
        }
    }

    async deleteReservation(reservationId: number): Promise<boolean> {
        try {
            await reservationsApi.delete(reservationId);
            toastStore.show('🗑️ Reserva eliminada correctamente', 'success');
            await reservationStore.refresh();
            return true;
        } catch (error: any) {
            console.error('Error deleting reservation:', error);
            const message = error.response?.data?.detail || 'Error al eliminar la reserva';
            toastStore.show(message, 'error');
            return false;
        }
    }

    // Getters
    get isValid(): boolean { return this.isValidForm; }
    get canSearchAvailability(): boolean { return this.canFetchSlots; }
}

export const reservationForm = new ReservationFormManager();
