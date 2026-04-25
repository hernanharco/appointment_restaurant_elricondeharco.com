<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
  export let isOpen = false;
  export let reservation = null;
  export let mode = 'create'; // create, edit, view
  
  const dispatch = createEventDispatcher();
  
  let formData = {
    client_name: '',
    client_phone: '',
    client_email: '',
    client_notes: '',
    party_size: 2,
    start_time: '',
    end_time: ''
  };
  
  let isSubmitting = false;
  let error = '';
  
  // Reset form when modal opens
  $: if (isOpen) {
    if (mode === 'edit' && reservation) {
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
      formData = {
        client_name: '',
        client_phone: '',
        client_email: '',
        client_notes: '',
        party_size: 2,
        start_time: '',
        end_time: ''
      };
    }
    error = '';
  }
  
  function formatDateTimeForInput(dateTimeStr) {
    if (!dateTimeStr) return '';
    const date = new Date(dateTimeStr);
    return date.toISOString().slice(0, 16);
  }
  
  function calculateEndTime() {
    if (formData.start_time) {
      const startTime = new Date(formData.start_time);
      const endTime = new Date(startTime.getTime() + 2 * 60 * 60 * 1000); // 2 hours default
      formData.end_time = endTime.toISOString().slice(0, 16);
    }
  }
  
  async function handleSubmit() {
    if (isSubmitting) return;
    
    isSubmitting = true;
    error = '';
    
    try {
      const url = mode === 'create' 
        ? '/api/v1/reservations/'
        : `/api/v1/reservations/${reservation.id}`;
      
      const method = mode === 'create' ? 'POST' : 'PUT';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al guardar la reserva');
      }
      
      const result = await response.json();
      dispatch('success', result);
      closeModal();
      
    } catch (err) {
      error = err.message || 'Error al procesar la solicitud';
    } finally {
      isSubmitting = false;
    }
  }
  
  function closeModal() {
    isOpen = false;
    dispatch('close');
  }
  
  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }
</script>

{#if isOpen}
  <div 
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    on:click={handleBackdropClick}
  >
    <div class="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-slate-800">
            {mode === 'create' ? 'Nueva Reserva' : mode === 'edit' ? 'Editar Reserva' : 'Ver Reserva'}
          </h2>
          <button 
            on:click={closeModal}
            class="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        
        {#if error}
          <div class="mb-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        {/if}
        
        <form on:submit|preventDefault={handleSubmit}>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Nombre del Cliente *
              </label>
              <input
                type="text"
                bind:value={formData.client_name}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Teléfono
              </label>
              <input
                type="tel"
                bind:value={formData.client_phone}
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Email
              </label>
              <input
                type="email"
                bind:value={formData.client_email}
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Número de Personas *
              </label>
              <input
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
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Fecha y Hora de Inicio *
              </label>
              <input
                type="datetime-local"
                bind:value={formData.start_time}
                on:change={calculateEndTime}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Fecha y Hora de Fin *
              </label>
              <input
                type="datetime-local"
                bind:value={formData.end_time}
                required
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">
                Notas
              </label>
              <textarea
                bind:value={formData.client_notes}
                rows="3"
                disabled={mode === 'view'}
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              ></textarea>
            </div>
          </div>
          
          {#if mode !== 'view'}
            <div class="flex gap-3 mt-6">
              <button
                type="button"
                on:click={closeModal}
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {isSubmitting ? 'Guardando...' : (mode === 'create' ? 'Crear Reserva' : 'Actualizar')}
              </button>
            </div>
          {:else}
            <div class="mt-6">
              <button
                type="button"
                on:click={closeModal}
                class="w-full px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors"
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
