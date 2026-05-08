<script lang="ts">
  import { reservationStore } from '@/lib/stores/reservation-state.svelte';

  // Generate days for current week based on store's selectedDate
  function getWeekDays(date: Date) {
    const days = [];
    const startOfWeek = new Date(date);
    const day = startOfWeek.getDay();
    const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1);
    startOfWeek.setDate(diff);

    for (let i = 0; i < 7; i++) {
      const d = new Date(startOfWeek);
      d.setDate(startOfWeek.getDate() + i);
      days.push(d);
    }
    return days;
  }

  function formatDate(date: Date) {
    return date.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
    });
  }

  function formatDayName(date: Date) {
    return date.toLocaleDateString('es-ES', {
      weekday: 'short',
    });
  }

  function isToday(date: Date) {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  }

  function isSelected(date: Date) {
    return date.toDateString() === reservationStore.selectedDate.toDateString();
  }

  function selectDate(date: Date) {
    reservationStore.setSelectedDate(date);
  }

  function previousWeek() {
    const newDate = new Date(reservationStore.selectedDate);
    newDate.setDate(newDate.getDate() - 7);
    reservationStore.setSelectedDate(newDate);
  }

  function nextWeek() {
    const newDate = new Date(reservationStore.selectedDate);
    newDate.setDate(newDate.getDate() + 7);
    reservationStore.setSelectedDate(newDate);
  }

  // Derived state for week days
  let weekDays = $derived(getWeekDays(reservationStore.selectedDate));
</script>

<div class="days-view">
  <div class="flex items-center justify-between mb-4">
    <button onclick={previousWeek} class="p-2 hover:bg-slate-100 rounded-lg transition-colors flex items-center justify-center">
      <span class="material-symbols-outlined">chevron_left</span>
    </button>

    <div class="flex gap-1 overflow-x-auto no-scrollbar">
      {#each weekDays as date (date.toISOString())}
        <button
          onclick={() => selectDate(date)}
          class="flex flex-col items-center p-3 rounded-lg min-w-[60px] transition-all {isSelected(date)
            ? 'bg-blue-600 text-white shadow-md transform scale-105'
            : isToday(date)
              ? 'bg-blue-50 text-blue-700 border border-blue-100'
              : 'hover:bg-slate-100 text-slate-700'}"
        >
          <span class="text-[10px] uppercase tracking-wider font-bold opacity-80">{formatDayName(date)}</span>
          <span class="text-lg font-bold mt-0.5">{formatDate(date).split(' ')[0]}</span>
          <span class="text-[10px] font-medium opacity-80">{formatDate(date).split(' ')[1]}</span>
          {#if isToday(date) && !isSelected(date)}
            <div class="w-1 h-1 bg-blue-600 rounded-full mt-1"></div>
          {/if}
        </button>
      {/each}
    </div>

    <button onclick={nextWeek} class="p-2 hover:bg-slate-100 rounded-lg transition-colors flex items-center justify-center">
      <span class="material-symbols-outlined">chevron_right</span>
    </button>
  </div>

  <div class="text-center text-sm font-medium text-slate-500 bg-slate-50 py-2 rounded-full capitalize">
    {reservationStore.selectedDate.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })}
  </div>
</div>

<style>
  .days-view {
    @apply w-full;
  }
  
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
