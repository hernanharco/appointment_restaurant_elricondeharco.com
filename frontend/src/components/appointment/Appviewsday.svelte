<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let selectedDate: Date = new Date();
  const dispatch = createEventDispatcher();

  // Generate days for current week
  function getWeekDays() {
    const days = [];
    const startOfWeek = new Date(selectedDate);
    const day = startOfWeek.getDay();
    const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1);
    startOfWeek.setDate(diff);

    for (let i = 0; i < 7; i++) {
      const date = new Date(startOfWeek);
      date.setDate(startOfWeek.getDate() + i);
      days.push(date);
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
    return date.toDateString() === selectedDate.toDateString();
  }

  function selectDate(date: Date) {
    selectedDate = date;
    dispatch('dateSelected', date);
  }

  function previousWeek() {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() - 7);
    selectedDate = newDate;
  }

  function nextWeek() {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + 7);
    selectedDate = newDate;
  }

  $: weekDays = getWeekDays();
</script>

<div class="days-view">
  <div class="flex items-center justify-between mb-4">
    <button on:click={previousWeek} class="p-2 hover:bg-slate-100 rounded-lg transition-colors">
      <span class="material-symbols-outlined">chevron_left</span>
    </button>

    <div class="flex gap-1">
      {#each weekDays as date (date.toISOString())}
        <button
          on:click={() => selectDate(date)}
          class="flex flex-col items-center p-3 rounded-lg min-w-[60px] transition-colors {isSelected(
            date,
          )
            ? 'bg-blue-600 text-white'
            : isToday(date)
              ? 'bg-blue-100 text-blue-700'
              : 'hover:bg-slate-100 text-slate-700'}"
        >
          <span class="text-xs font-medium">{formatDayName(date)}</span>
          <span class="text-lg font-bold mt-1">{formatDate(date)}</span>
          {#if isToday(date) && !isSelected(date)}
            <div class="w-1 h-1 bg-blue-600 rounded-full mt-1"></div>
          {/if}
        </button>
      {/each}
    </div>

    <button on:click={nextWeek} class="p-2 hover:bg-slate-100 rounded-lg transition-colors">
      <span class="material-symbols-outlined">chevron_right</span>
    </button>
  </div>

  <div class="text-center text-sm text-slate-600">
    {selectedDate.toLocaleDateString('es-ES', {
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
</style>
