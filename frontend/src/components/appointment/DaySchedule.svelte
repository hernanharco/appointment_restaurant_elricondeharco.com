<script lang="ts">
  import { onMount } from 'svelte';
  import apiCentralized from '@/services/api-centralized.ts';
  import { reservationStore } from '@/lib/stores/reservation-state.svelte';
  import ReservationModal from './ReservationModal.svelte';

  let reservations = $state<any[]>([]);
  let selectedAppointment = $state<any>(null);
  let isModalOpen = $state(false);
  let modalMode = $state<'create' | 'edit' | 'view'>('create');
  let loading = $state(false);
  let error = $state('');

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
      const dateStr = reservationStore.selectedDate.toISOString().split('T')[0] || '';
      reservations = await apiCentralized.getReservationsByDate(dateStr);
    } catch (err) {
      error = (err as Error).message || 'Error al cargar las reservas';
      console.error('Error loading reservations:', err);
    } finally {
      loading = false;
    }
  }

  function getReservationForTime(time: string): any {
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

  function selectReservation(reservation: any) {
    selectedAppointment = reservation;
    modalMode = 'view';
    isModalOpen = true;
  }

  function editReservation(reservation: any) {
    selectedAppointment = reservation;
    modalMode = 'edit';
    isModalOpen = true;
  }

  function createNewReservation(time: string): void {
    selectedAppointment = null;
    modalMode = 'create';
    isModalOpen = true;
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

  function isPastTime(time: string): boolean {
    const [hour, minute] = time.split(':').map(Number);
    const slotDate = new Date(reservationStore.selectedDate);
    if (hour && minute) {
      slotDate.setHours(hour, minute, 0, 0);
    }

    return slotDate < new Date();
  }

  const timeSlots = generateTimeSlots();

  // Load reservations when selected date changes
  $effect(() => {
    loadReservations();
  });

  // Add event listeners for modal events
  onMount(() => {
    const interval = setInterval(() => {
      // Update current time if needed
    }, 60000);

    const modalSuccessHandler = () => {
      handleModalSuccess();
    };

    const modalCloseHandler = () => {
      handleModalClose();
    };

    // Listen for open reservation modal from header
    const openReservationModalHandler = (evt: Event) => {
      const customEvent = evt as CustomEvent;
      const { mode, time } = customEvent.detail || {};
      if (mode === 'create') {
        createNewReservation(time);
      }
    };

    document.addEventListener('modalSuccess', modalSuccessHandler);
    document.addEventListener('modalClose', modalCloseHandler);
    document.addEventListener('openReservationModal', openReservationModalHandler);

    return () => {
      clearInterval(interval);
      document.removeEventListener('modalSuccess', modalSuccessHandler);
      document.removeEventListener('modalClose', modalCloseHandler);
      document.removeEventListener('openReservationModal', openReservationModalHandler);
    };
  });

  // Handle modal events
  function handleModalSuccess(): void {
    isModalOpen = false;
    loadReservations(); // Reload reservations after successful operation
  }

  function handleModalClose(): void {
    isModalOpen = false;
  }

  // Event handlers for modal (not used for now)
  // function modalSuccess(event: any): void {
  //   handleModalSuccess();
  // }

  // function modalClose(event: any): void {
  //   handleModalClose();
  // }
</script>

<div class="day-schedule">
  <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
    <div class="p-5 border-b border-slate-200 bg-slate-50/50">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-slate-800">Horario del Día</h2>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5">
            <div class="w-2.5 h-2.5 bg-green-500 rounded-full"></div>
            <span class="text-[11px] font-medium text-slate-500">Confirmada</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-2.5 h-2.5 bg-blue-500 rounded-full"></div>
            <span class="text-[11px] font-medium text-slate-500">Programada</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-2.5 h-2.5 bg-orange-500 rounded-full"></div>
            <span class="text-[11px] font-medium text-slate-500">En curso</span>
          </div>
        </div>
      </div>
    </div>

    <div class="max-h-[700px] overflow-y-auto custom-scrollbar">
      {#each timeSlots as time (time)}
        {@const reservation = getReservationForTime(time)}
        {@const isPast = isPastTime(time)}
        <div
          class="flex border-b border-slate-50 group transition-colors {isPast
            ? 'bg-slate-50/30'
            : 'hover:bg-blue-50/30'}"
        >
          <div
            class="w-20 px-4 py-6 text-sm font-bold {isPast
              ? 'text-slate-400'
              : 'text-slate-600'} border-r border-slate-50 flex items-center justify-center"
          >
            {time}
          </div>

          <div class="flex-1 p-2">
            {#if reservation}
              <button
                class="w-full text-left p-4 rounded-xl border-2 transition-all hover:shadow-md {getStatusColor(
                  reservation.status,
                )} flex items-center justify-between group/card"
                onclick={() => selectReservation(reservation)}
              >
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-base">{reservation.client_name}</span>
                    <span
                      class="px-2 py-0.5 rounded-full bg-white/50 text-[10px] font-bold uppercase tracking-tight"
                    >
                      {reservation.party_size} pax
                    </span>
                  </div>
                  <div class="flex items-center gap-3 mt-2">
                    <div class="flex items-center gap-1 text-xs font-medium opacity-80">
                      <span class="material-symbols-outlined text-sm">schedule</span>
                      {formatDuration(reservation.start_time, reservation.end_time)}
                    </div>
                    <div class="flex items-center gap-1 text-xs font-medium opacity-80">
                      <span class="material-symbols-outlined text-sm">info</span>
                      {getStatusText(reservation.status)}
                    </div>
                  </div>
                  {#if reservation.client_notes}
                    <div class="text-xs mt-3 opacity-70 italic line-clamp-1">
                      "{reservation.client_notes}"
                    </div>
                  {/if}
                </div>

                <div
                  class="flex flex-col gap-2 opacity-0 group-hover/card:opacity-100 transition-opacity"
                >
                  <div
                    class="p-2 hover:bg-white/50 rounded-lg transition-colors cursor-pointer"
                    onclick={() => {
                      editReservation(reservation);
                    }}
                    role="button"
                    tabindex="0"
                    onkeydown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        editReservation(reservation);
                      }
                    }}
                  >
                    <span class="material-symbols-outlined text-lg">edit</span>
                  </div>
                </div>
              </button>
            {:else}
              <button
                class="w-full h-full min-h-[60px] flex items-center justify-center gap-2 border-2 border-dashed border-slate-200 rounded-xl text-slate-400 hover:border-blue-300 hover:text-blue-500 hover:bg-blue-50/50 transition-all group/btn"
                onclick={() => createNewReservation(time)}
              >
                <span
                  class="material-symbols-outlined text-lg group-hover/btn:scale-110 transition-transform"
                  >add_circle</span
                >
                <span class="text-sm font-bold tracking-tight">Reservar</span>
              </button>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<ReservationModal bind:isOpen={isModalOpen} reservation={selectedAppointment} mode={modalMode} />

<style>
  .day-schedule {
    width: 100%;
  }

  .custom-scrollbar::-webkit-scrollbar {
    width: 8px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 20px;
    border: 2px solid transparent;
    background-clip: content-box;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #cbd5e1;
    background-clip: content-box;
  }
</style>
