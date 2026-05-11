<script lang="ts">
  import apiCentralized, { type ReservationData } from '@/services/api-centralized.ts';
  
  import { reservationStore } from '@/lib/stores/reservation-state.svelte';

  let { 
    isOpen = $bindable(false), 
    reservation = $bindable(null), 
    mode = $bindable('create'), // create, edit, view
    preselectedTime = $bindable('') // hora seleccionada desde el slot "12:00"
  } = $props();
  
  let formData = $state({
    client_name: '',
    client_phone: '',
    client_email: '',
    client_notes: '',
    party_size: 2,
    start_time: '',
    end_time: ''
  });
  
  let isSubmitting = $state(false);
  let isDeleting = $state(false);
  let showDeleteConfirm = $state(false);
  let error = $state('');
  
  // Reset form when modal opens
  $effect(() => {
    if (isOpen) {
      if ((mode === 'edit' || mode === 'view') && reservation) {
        formData = {
          client_name: reservation.client_name || '',
          client_phone: reservation.client_phone || '',
          client_email: reservation.client_email || '',
          client_notes: reservation.client_notes || '',
          party_size: reservation.party_size || 2,
          start_time: formatDateTimeForInput(reservation.start_time),
          end_time: formatDateTimeForInput(reservation.end_time)
        };
      } else {
        // Pre-fill start_time if coming from a time slot click
        let startTime = '';
        if (preselectedTime) {
          const dateStr = reservationStore.selectedDate.toISOString().split('T')[0];
          startTime = `${dateStr}T${preselectedTime}`;
        }

        formData = {
          client_name: '',
          client_phone: '',
          client_email: '',
          client_notes: '',
          party_size: 2,
          start_time: startTime,
          end_time: ''
        };

        // Auto-calculate end_time if start_time was prefilled
        if (startTime) {
          calculateEndTime();
        }
      }
      error = '';
    }
  });

  /** Convierte fecha ISO de la API (UTC) a string local para datetime-local input */
  function formatDateTimeForInput(dateTimeStr: any): string {
    if (!dateTimeStr) return '';
    const d = new Date(dateTimeStr);
    // .toISOString() devuelve UTC, pero datetime-local necesita HORA LOCAL
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }
  
  /** Convierte string datetime-local a UTC ISO (sin Z, para enviar al backend) */
  function toUtcString(localDateTime: string): string {
    if (!localDateTime) return '';
    const d = new Date(localDateTime);
    return d.toISOString().slice(0, 19); // "2026-05-11T10:00:00" (UTC sin Z)
  }

  function calculateEndTime(): void {
    if (formData.start_time) {
      const startTime = new Date(formData.start_time);
      const endTime = new Date(startTime.getTime() + 2 * 60 * 60 * 1000); // 2 hours default
      // Mantenemos formato local (la conversión a UTC se hace en handleSubmit)
      const year = endTime.getFullYear();
      const month = String(endTime.getMonth() + 1).padStart(2, '0');
      const day = String(endTime.getDate()).padStart(2, '0');
      const hours = String(endTime.getHours()).padStart(2, '0');
      const minutes = String(endTime.getMinutes()).padStart(2, '0');
      formData.end_time = `${year}-${month}-${day}T${hours}:${minutes}`;
    }
  }
  
  async function handleSubmit(): Promise<void> {
    if (isSubmitting) return;
    
    isSubmitting = true;
    error = '';
    
    try {
      let result;
      
      // Convertir horas locales a UTC antes de enviar al backend
      const payload = {
        ...formData,
        start_time: toUtcString(formData.start_time) || formData.start_time,
        end_time: toUtcString(formData.end_time) || formData.end_time,
      };
      
      if (mode === 'create') {
        result = await apiCentralized.createReservation(payload as ReservationData);
      } else if (mode === 'edit' && reservation) {
        result = await apiCentralized.updateReservation(reservation.id, payload as Partial<ReservationData>);
      }
      
      // Success - notify parent component
      isOpen = false;
      
      // Dispatch custom event for parent component
      const event = new CustomEvent('modalSuccess', { detail: result });
      document.dispatchEvent(event);
      
    } catch (err) {
      error = (err as Error).message || 'Error al procesar la solicitud';
    } finally {
      isSubmitting = false;
    }
  }

  async function handleDelete(): Promise<void> {
    if (isDeleting || !reservation) return;
    
    isDeleting = true;
    error = '';
    
    try {
      await apiCentralized.cancelReservation(reservation.id);
      
      isOpen = false;
      showDeleteConfirm = false;
      
      const event = new CustomEvent('modalSuccess');
      document.dispatchEvent(event);
      
    } catch (err) {
      error = (err as Error).message || 'Error al cancelar la reserva';
    } finally {
      isDeleting = false;
    }
  }

  function confirmDelete(): void {
    showDeleteConfirm = true;
  }

  function cancelDelete(): void {
    showDeleteConfirm = false;
  }
  
  function switchToEdit(): void {
    mode = 'edit';
  }

  function closeModal(): void {
    isOpen = false;
    
    // Dispatch custom event for parent component
    const event = new CustomEvent('modalClose');
    document.dispatchEvent(event);
  }
  
  function handleBackdropClick(event: MouseEvent): void {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }
</script>

{#if isOpen}
  <div 
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    onclick={handleBackdropClick}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
  >
    <div class="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 id="modal-title" class="text-xl font-semibold text-slate-800">
            {mode === 'create' ? 'Nueva Reserva' : mode === 'edit' ? 'Editar Reserva' : 'Ver Reserva'}
          </h2>
          <button 
            onclick={closeModal}
            class="text-slate-400 hover:text-slate-600 transition-colors"
            aria-label="Cerrar modal"
          >
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        
        {#if error}
          <div class="mb-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        {/if}
        
        <form onsubmit={handleSubmit}>
          <div class="space-y-4">
            <div>
              <label for="client_name" class="block text-sm font-medium text-slate-700 mb-1">
                Nombre del Cliente *
              </label>
              <input
                id="client_name"
                type="text"
                bind:value={formData.client_name}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="client_phone" class="block text-sm font-medium text-slate-700 mb-1">
                Teléfono
              </label>
              <input
                id="client_phone"
                type="tel"
                bind:value={formData.client_phone}
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="client_email" class="block text-sm font-medium text-slate-700 mb-1">
                Email
              </label>
              <input
                id="client_email"
                type="email"
                bind:value={formData.client_email}
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="party_size" class="block text-sm font-medium text-slate-700 mb-1">
                Número de Personas *
              </label>
              <input
                id="party_size"
                type="number"
                bind:value={formData.party_size}
                min="1"
                max="20"
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="start_time" class="block text-sm font-medium text-slate-700 mb-1">
                Fecha y Hora de Inicio *
              </label>
              <input
                id="start_time"
                type="datetime-local"
                bind:value={formData.start_time}
                oninput={calculateEndTime}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="end_time" class="block text-sm font-medium text-slate-700 mb-1">
                Fecha y Hora de Fin *
              </label>
              <input
                id="end_time"
                type="datetime-local"
                bind:value={formData.end_time}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label for="client_notes" class="block text-sm font-medium text-slate-700 mb-1">
                Notas
              </label>
              <textarea
                id="client_notes"
                bind:value={formData.client_notes}
                rows="3"
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              ></textarea>
            </div>
          </div>
          
          {#if showDeleteConfirm}
            <div class="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <p class="text-sm font-medium text-red-800 mb-3">
                ¿Estás seguro de cancelar esta reserva?
              </p>
              <div class="flex gap-3">
                <button
                  type="button"
                  onclick={cancelDelete}
                  disabled={isDeleting}
                  class="flex-1 px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-white transition-colors disabled:opacity-50"
                >
                  No, mantener
                </button>
                <button
                  type="button"
                  onclick={handleDelete}
                  disabled={isDeleting}
                  class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {#if isDeleting}
                    Cancelando...
                  {:else}
                    <span class="material-symbols-outlined text-sm">delete</span>
                    Sí, cancelar
                  {/if}
                </button>
              </div>
            </div>
          {:else if mode === 'create'}
            <div class="flex gap-3 mt-6">
              <button
                type="button"
                onclick={closeModal}
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {#if isSubmitting}
                  Guardando...
                {:else}
                  <span class="material-symbols-outlined text-sm">add</span>
                  Crear Reserva
                {/if}
              </button>
            </div>
          {:else if mode === 'edit'}
            <div class="flex gap-3 mt-6">
              <button
                type="button"
                onclick={closeModal}
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                type="button"
                onclick={confirmDelete}
                disabled={isSubmitting}
                class="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <span class="material-symbols-outlined text-sm">delete</span>
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {#if isSubmitting}
                  Guardando...
                {:else}
                  <span class="material-symbols-outlined text-sm">save</span>
                  Actualizar
                {/if}
              </button>
            </div>
          {:else}
            <div class="mt-6 flex gap-3">
              <button
                type="button"
                onclick={switchToEdit}
                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
              >
                <span class="material-symbols-outlined text-sm">edit</span>
                Editar Reserva
              </button>
              <button
                type="button"
                onclick={closeModal}
                class="px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors"
              >
                Cerrar
              </button>
            </div>
          {/if}
        </form>
      </div>
    </div>
  </div>
{/if}
