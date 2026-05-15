<script lang="ts">
  import { onMount } from 'svelte';
  import apiCentralized from '@/services/api-centralized.ts';
  import { reservationStore } from '@/lib/stores/reservation-state.svelte';
  import ReservationModal from './ReservationModal.svelte';

  let reservations = $state<any[]>([]);
  let selectedAppointment = $state<any>(null);
  let isModalOpen = $state(false);
  let modalMode = $state<'create' | 'edit' | 'view'>('create');
  let selectedTime = $state<string>('');
  let loading = $state(false);
  let error = $state('');

  // Slots expandidos (con 2+ reservas)
  let expandedSlots = $state(new Set<string>());

  function toggleSlot(time: string) {
    if (expandedSlots.has(time)) {
      expandedSlots.delete(time);
    } else {
      expandedSlots.add(time);
    }
    // Forzar reactividad con nuevo Set
    expandedSlots = new Set(expandedSlots);
  }

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
      const all = await apiCentralized.getReservationsByDate(dateStr);
      // Filtrar solo reservas activas (no canceladas ni no-show)
      reservations = all.filter(r => r.status !== 'cancelled' && r.status !== 'no_show');
    } catch (err) {
      error = (err as Error).message || 'Error al cargar las reservas';
      console.error('Error loading reservations:', err);
    } finally {
      loading = false;
    }
  }

  function getReservationsForTime(time: string): any[] {
    return reservations.filter((reservation) => {
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
    selectedTime = time;
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

  function getWhatsAppUrl(phone: string): string {
    // Limpiar: dejar solo dígitos
    const clean = phone.replace(/\D/g, '');
    return clean ? `https://wa.me/${clean}` : '#';
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

  // Auto-scroll al slot de la hora actual
  function scrollToCurrentTime(): void {
    const now = new Date();
    const currentHour = now.getHours();
    const currentMin = now.getMinutes();

    // Redondear al slot de 30 min más cercano hacia abajo
    const roundedMin = Math.floor(currentMin / 30) * 30;
    const timeStr = `${String(currentHour).padStart(2, '0')}:${String(roundedMin).padStart(2, '0')}`;

    // Si la fecha seleccionada NO es hoy, no scrolleamos
    const today = new Date();
    if (reservationStore.selectedDate.toDateString() !== today.toDateString()) return;

    requestAnimationFrame(() => {
      const container = document.getElementById('schedule-scroll-container');
      if (!container) return;

      const slot = container.querySelector(`[data-time="${timeStr}"]`);
      if (slot) {
        slot.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }
    });
  }

  // Load reservations when selected date changes
  $effect(() => {
    loadReservations();
  });

  // Auto-scroll al slot actual cuando se cargan las reservas
  $effect(() => {
    if (reservations.length >= 0) {
      // Usamos requestAnimationFrame para esperar que el DOM se actualice
      requestAnimationFrame(() => scrollToCurrentTime());
    }
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

    <div id="schedule-scroll-container" class="max-h-[700px] overflow-y-auto custom-scrollbar">
      {#each timeSlots as time (time)}
        {@const slotReservations = getReservationsForTime(time)}
        {@const count = slotReservations.length}
        {@const isPast = isPastTime(time)}
        {@const isExpanded = expandedSlots.has(time)}
        {@const totalPeople = slotReservations.reduce((sum, r) => sum + (r.party_size || 0), 0)}
        <div
          data-time={time}
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
            {#if count === 0}
              <!-- Slot vacío → botón Reservar -->
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

            {:else if count === 1}
              <!-- 1 reserva → tarjeta completa -->
              {@const s = slotReservations[0]}
              <button
                class="w-full text-left p-4 rounded-xl border-2 transition-all hover:shadow-md {getStatusColor(
                  s.status,
                )} flex items-start justify-between group/card"
                onclick={() => selectReservation(s)}
              >
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-base text-slate-800 truncate">{s.client_name}</span>
                    <span
                      class="shrink-0 px-2 py-0.5 rounded-full bg-white/50 text-[10px] font-bold uppercase tracking-tight"
                    >
                      {s.party_size} pax
                    </span>
                  </div>

                  {#if s.client_phone}
                    <a
                      href={getWhatsAppUrl(s.client_phone)}
                      target="_blank"
                      rel="noopener noreferrer"
                      onclick={(e) => e.stopPropagation()}
                      class="flex items-center gap-1.5 mt-1.5 text-xs font-medium text-green-600 hover:text-green-800 hover:underline transition-colors"
                    >
                      <span class="material-symbols-outlined text-sm">chat</span>
                      <span>{s.client_phone}</span>
                    </a>
                  {/if}

                  <div class="flex items-center gap-3 mt-2">
                    <div class="flex items-center gap-1 text-xs font-medium opacity-80">
                      <span class="material-symbols-outlined text-sm">schedule</span>
                      {formatDuration(s.start_time, s.end_time)}
                    </div>
                    <div class="flex items-center gap-1 text-xs font-medium opacity-80">
                      <span class="material-symbols-outlined text-sm">info</span>
                      {getStatusText(s.status)}
                    </div>
                  </div>
                  {#if s.client_notes}
                    <div class="text-xs mt-2.5 opacity-70 italic line-clamp-1">
                      "{s.client_notes}"
                    </div>
                  {/if}
                </div>

                <div
                  class="shrink-0 flex flex-col gap-1.5 ml-3 opacity-0 group-hover/card:opacity-100 transition-opacity"
                >
                  <div
                    class="p-2 hover:bg-white/50 rounded-lg transition-colors cursor-pointer"
                    onclick={() => {
                      editReservation(s);
                    }}
                    role="button"
                    tabindex="0"
                    onkeydown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        editReservation(s);
                      }
                    }}
                  >
                    <span class="material-symbols-outlined text-lg">edit</span>
                  </div>
                </div>
              </button>

            {:else}
              <!-- 2+ reservas → colapsable -->
              <div class="border-2 border-slate-200 rounded-xl overflow-hidden transition-all">
                <!-- Chip colapsado -->
                <button
                  class="w-full flex items-center justify-between gap-3 px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors"
                  onclick={() => toggleSlot(time)}
                >
                  <div class="flex items-center gap-2.5">
                    <span class="material-symbols-outlined text-lg text-slate-500">calendar_month</span>
                    <span class="text-sm font-bold text-slate-700">
                      {count} {count === 1 ? 'reserva' : 'reservas'}
                    </span>
                    <span class="px-2 py-0.5 rounded-full bg-white text-[10px] font-bold text-slate-500 border border-slate-200">
                      {totalPeople} pax
                    </span>
                  </div>
                  <div class="flex items-center gap-1.5 text-slate-400">
                    <span class="text-xs font-medium">{isExpanded ? 'Colapsar' : 'Ver'}</span>
                    <span
                      class="material-symbols-outlined text-lg transition-transform {isExpanded
                        ? 'rotate-180'
                        : ''}"
                    >
                      expand_more
                    </span>
                  </div>
                </button>

                <!-- Lista expandida -->
                {#if isExpanded}
                  <div class="divide-y divide-slate-100 border-t border-slate-200">
                    {#each slotReservations as s (s.id)}
                      <div
                        class="flex items-center justify-between px-4 py-3 hover:bg-blue-50/30 transition-colors cursor-pointer"
                        onclick={() => selectReservation(s)}
                      >
                        <div class="flex items-center gap-3 min-w-0">
                          <div
                            class="w-1.5 h-8 rounded-full shrink-0 {s.status === 'confirmed'
                              ? 'bg-green-500'
                              : 'bg-blue-500'}"
                          ></div>
                          <div class="min-w-0">
                            <div class="flex items-center gap-2">
                              <span class="font-bold text-sm text-slate-800 truncate">{s.client_name}</span>
                              <span
                                class="px-1.5 py-0.5 rounded bg-slate-100 text-[10px] font-bold text-slate-600"
                              >
                                {s.party_size} pax
                              </span>
                            </div>
                            <div class="flex items-center gap-3 mt-0.5">
                              {#if s.client_phone}
                                <a
                                  href={getWhatsAppUrl(s.client_phone)}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  onclick={(e) => e.stopPropagation()}
                                  class="text-[11px] text-green-600 hover:text-green-800 hover:underline flex items-center gap-1"
                                >
                                  <span class="material-symbols-outlined text-xs">chat</span>
                                  {s.client_phone}
                                </a>
                              {/if}
                              {#if s.client_notes}
                                <span class="text-[11px] text-slate-400 truncate max-w-[120px]">
                                  "{s.client_notes}"
                                </span>
                              {/if}
                            </div>
                          </div>
                        </div>
                        <div
                          class="shrink-0 p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                          onclick={(e) => {
                            e.stopPropagation();
                            editReservation(s);
                          }}
                          role="button"
                          tabindex="0"
                          onkeydown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                              e.stopPropagation();
                              editReservation(s);
                            }
                          }}
                        >
                          <span class="material-symbols-outlined text-base">edit</span>
                        </div>
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

{#if isModalOpen}
  <ReservationModal reservation={selectedAppointment} mode={modalMode} preselectedTime={selectedTime} onClose={() => isModalOpen = false} />
{/if}

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
