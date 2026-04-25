<script lang="ts">
  import { onMount } from 'svelte';
  import apiService from '@/services/api.js';
  import ReservationModal from './ReservationModal.svelte';

  export let selectedDate = new Date();

  let reservations = [];
  let selectedAppointment = null;
  let isModalOpen = false;
  let modalMode = 'create';
  let loading = false;
  let error = '';
  let currentTime = new Date();

  // Generate time slots from 8:00 to 20:00
  function generateTimeSlots() {
    const slots = [];
    for (let hour = 8; hour <= 20; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const time = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        slots.push(time);
      }
    }
    return slots;
  }

  // Load reservations for selected date
  async function loadReservations() {
    loading = true;
    error = '';

    try {
      const dateStr = selectedDate.toISOString().split('T')[0];
      reservations = await apiService.getReservations(dateStr);
    } catch (err) {
      error = err.message || 'Error al cargar las reservas';
      console.error('Error loading reservations:', err);
    } finally {
      loading = false;
    }
  }

  function getReservationForTime(time: string) {
    return reservations.find((reservation) => {
      const startTime = new Date(reservation.start_time);
      const timeStr = `${startTime.getHours().toString().padStart(2, '0')}:${startTime.getMinutes().toString().padStart(2, '0')}`;
      return timeStr === time;
    });
  }

  function getStatusColor(status: string) {
    switch (status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'in_progress':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'completed':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      case 'cancelled':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'no_show':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  }

  function getStatusText(status: string) {
    switch (status) {
      case 'confirmed':
        return 'Confirmada';
      case 'scheduled':
        return 'Programada';
      case 'in_progress':
        return 'En curso';
      case 'completed':
        return 'Completada';
      case 'cancelled':
        return 'Cancelada';
      case 'no_show':
        return 'No asistió';
      default:
        return status;
    }
  }

  function selectReservation(reservation) {
    selectedAppointment = reservation;
    modalMode = 'view';
    isModalOpen = true;
  }

  function editReservation(reservation) {
    selectedAppointment = reservation;
    modalMode = 'edit';
    isModalOpen = true;
  }

  function createNewReservation(time: string) {
    selectedAppointment = null;
    modalMode = 'create';
    isModalOpen = true;

    // Pre-fill start time
    const [hours, minutes] = time.split(':').map(Number);
    const startTime = new Date(selectedDate);
    startTime.setHours(hours, minutes, 0, 0);

    // Set default end time (2 hours later)
    const endTime = new Date(startTime);
    endTime.setHours(endTime.getHours() + 2);
  }

  function formatDuration(startTime: string, endTime: string) {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const duration = (end.getTime() - start.getTime()) / (1000 * 60);

    if (duration >= 60) {
      const hours = Math.floor(duration / 60);
      const mins = duration % 60;
      return mins > 0 ? `${hours}h ${mins}min` : `${hours}h`;
    }
    return `${duration}min`;
  }

  function isCurrentTime(time: string) {
    const now = new Date();
    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();
    const [hour, minute] = time.split(':').map(Number);

    if (hour < currentHour || (hour === currentHour && minute < currentMinute)) {
      return true;
    }
    return false;
  }

  $: timeSlots = generateTimeSlots();

  // Load reservations when selected date changes
  $: if (selectedDate) {
    loadReservations();
  }

  // Update current time every minute
  onMount(() => {
    const interval = setInterval(() => {
      currentTime = new Date();
    }, 60000);

    return () => clearInterval(interval);
  });

  // Handle modal events
  function handleModalSuccess() {
    isModalOpen = false;
    loadReservations(); // Reload reservations after successful operation
  }

  function handleModalClose() {
    isModalOpen = false;
  }
</script>

<div class="day-schedule">
  <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
    <div class="p-4 border-b border-slate-200 bg-slate-50">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-slate-800">Horario del Día</h2>
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1">
            <div class="w-3 h-3 bg-green-100 border border-green-200 rounded"></div>
            <span class="text-xs text-slate-600">Confirmada</span>
          </div>
          <div class="flex items-center gap-1">
            <div class="w-3 h-3 bg-yellow-100 border border-yellow-200 rounded"></div>
            <span class="text-xs text-slate-600">Pendiente</span>
          </div>
          <div class="flex items-center gap-1">
            <div class="w-3 h-3 bg-blue-100 border border-blue-200 rounded"></div>
            <span class="text-xs text-slate-600">Completada</span>
          </div>
        </div>
      </div>
    </div>

    <div class="max-h-[600px] overflow-y-auto custom-scrollbar">
      {#each timeSlots as time (time)}
        {@const reservation = getReservationForTime(time)}
        <div
          class="flex border-b border-slate-100 hover:bg-slate-50 transition-colors {isCurrentTime(
            time,
          )
            ? 'bg-slate-50'
            : ''}"
        >
          <div class="w-20 px-3 py-3 text-sm font-medium text-slate-600 border-r border-slate-100">
            {time}
          </div>

          <div class="flex-1 px-3 py-2">
            {#if reservation}
              <div
                class="p-3 rounded-lg border cursor-pointer transition-all hover:shadow-sm {getStatusColor(
                  reservation.status,
                )}"
                on:click={() => selectReservation(reservation)}
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="font-medium text-sm">{reservation.client_name}</div>
                    <div class="text-xs mt-1 opacity-80">{reservation.party_size} personas</div>
                    <div class="flex items-center gap-2 mt-2">
                      <span class="text-xs font-medium">
                        {formatDuration(reservation.start_time, reservation.end_time)}
                      </span>
                      <span class="text-xs opacity-70">
                        • {getStatusText(reservation.status)}
                      </span>
                    </div>
                    {#if reservation.client_notes}
                      <div class="text-xs mt-2 opacity-70 italic">
                        "{reservation.client_notes}"
                      </div>
                    {/if}
                  </div>
                  <div class="flex gap-1">
                    <button
                      class="p-1 hover:bg-black hover:bg-opacity-10 rounded transition-colors"
                      on:click|stopPropagation={() => editReservation(reservation)}
                    >
                      <span class="material-symbols-outlined text-sm">edit</span>
                    </button>
                    <button
                      class="p-1 hover:bg-black hover:bg-opacity-10 rounded transition-colors"
                    >
                      <span class="material-symbols-outlined text-sm">more_vert</span>
                    </button>
                  </div>
                </div>
              </div>
            {:else}
              <div
                class="p-3 text-center text-slate-400 hover:text-slate-600 cursor-pointer transition-colors"
              >
                <button
                  class="flex items-center justify-center w-full py-2 border-2 border-dashed border-slate-300 rounded-lg hover:border-slate-400 hover:bg-slate-50 transition-all"
                  on:click={() => createNewReservation(time)}
                >
                  <span class="material-symbols-outlined text-sm mr-1">add</span>
                  <span class="text-sm">Nueva Reserva</span>
                </button>
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<ReservationModal
  bind:isOpen={isModalOpen}
  reservation={selectedAppointment}
  mode={modalMode}
  on:success={handleModalSuccess}
  on:close={handleModalClose}
/>

<style>
  .day-schedule {
    @apply w-full;
  }

  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
</style>
