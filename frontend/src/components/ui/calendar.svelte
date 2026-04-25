<script lang="ts">
  import { cn } from "../../lib/utils";
  import { ChevronLeft, ChevronRight } from "lucide-svelte";
  
  // Svelte 5: Definimos las props con Runes
  // selected = $bindable() permite que los cambios aquí se vean en el Dashboard automáticamente
  let { 
    selected = $bindable(new Date()), 
    class: className = '', 
    disabled = false 
  } = $props();
  
  // Estado interno con Runes
  let currentMonth = $state(new Date());
  
  // Lógica reactiva con $derived (reemplaza a $:)
  let monthYear = $derived(
    currentMonth.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' })
  );
  
  let days = $derived.by(() => {
    const monthStart = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
    const startDate = new Date(monthStart);
    startDate.setDate(startDate.getDate() - startDate.getDay());
    
    return Array.from({ length: 42 }, (_, i) => {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      return date;
    });
  });
  
  // Funciones de navegación
  function previousMonth() {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1);
  }
  
  function nextMonth() {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
  }
  
  function selectDate(date: Date) {
    if (disabled) return;
    selected = date; // Al ser $bindable, actualiza el Dashboard automáticamente
  }

  // Helpers de estado
  const isSameMonth = (date: Date) => 
    date.getMonth() === currentMonth.getMonth() && date.getFullYear() === currentMonth.getFullYear();

  const isToday = (date: Date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isSelected = (date: Date) => 
    selected && date.toDateString() === selected.toDateString();
</script>

<div class={cn("p-3 space-y-4 bg-white", className)}>
  <div class="flex items-center justify-between">
    <h2 class="text-sm font-semibold capitalize">{monthYear}</h2>
    <div class="flex items-center space-x-1">
      <button
        type="button"
        class="h-7 w-7 inline-flex items-center justify-center rounded-md border hover:bg-slate-100 disabled:opacity-50"
        onclick={previousMonth}
        {disabled}
      >
        <ChevronLeft class="h-4 w-4" />
      </button>
      <button
        type="button"
        class="h-7 w-7 inline-flex items-center justify-center rounded-md border hover:bg-slate-100 disabled:opacity-50"
        onclick={nextMonth}
        {disabled}
      >
        <ChevronRight class="h-4 w-4" />
      </button>
    </div>
  </div>
  
  <div class="grid grid-cols-7 gap-1 text-center text-[10px] font-medium text-slate-500">
    <div>Dom</div><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div>
  </div>
  
  <div class="grid grid-cols-7 gap-1">
    {#each days as date}
      <button
        type="button"
        onclick={() => selectDate(date)}
        disabled={disabled || !isSameMonth(date)}
        class={cn(
          "h-8 w-8 text-center text-sm rounded-md transition-all",
          !isSameMonth(date) && "text-slate-300 pointer-events-none",
          isToday(date) && !isSelected(date) && "bg-slate-100 text-slate-900 font-bold",
          isSelected(date) && "bg-slate-900 text-white font-medium",
          !isSelected(date) && isSameMonth(date) && "hover:bg-slate-100 text-slate-700"
        )}
      >
        {date.getDate()}
      </button>
    {/each}
  </div>
</div>