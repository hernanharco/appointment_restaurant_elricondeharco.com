<script lang="ts">
  import { onMount } from 'svelte';
  import apiCentralized from '@/services/api-centralized.ts';

  let { isOpen = $bindable(false) } = $props();

  let config = $state({
    restaurantName: 'Mi Restaurante',
    maxCapacity: 50, // Capacidad máxima de personas
    openingTime: '08:00',
    closingTime: '22:00',
    averageTurnTime: 120, // minutos por turno
    daysOfWeek: [
      { day: 1, name: 'Lunes', isOpen: true, openTime: '08:00', closeTime: '22:00' },
      { day: 2, name: 'Martes', isOpen: true, openTime: '08:00', closeTime: '22:00' },
      { day: 3, name: 'Miércoles', isOpen: true, openTime: '08:00', closeTime: '22:00' },
      { day: 4, name: 'Jueves', isOpen: true, openTime: '08:00', closeTime: '22:00' },
      { day: 5, name: 'Viernes', isOpen: true, openTime: '08:00', closeTime: '23:00' },
      { day: 6, name: 'Sábado', isOpen: true, openTime: '09:00', closeTime: '23:00' },
      { day: 0, name: 'Domingo', isOpen: false, openTime: '09:00', closeTime: '15:00' },
    ],
  });

  let isSubmitting = $state(false);
  let error = $state('');
  let success = $state('');

  function closeModal(): void {
    isOpen = false;
    error = '';
    success = '';
  }

  function handleBackdropClick(event: MouseEvent): void {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }

  async function handleSave(): Promise<void> {
    if (isSubmitting) return;

    isSubmitting = true;
    error = '';
    success = '';

    try {
      // Guardar configuración en la API
      const configData = {
        name: config.restaurantName,
        max_capacity: config.maxCapacity,
        time_slot_duration_minutes: config.averageTurnTime,
        max_party_size: 20,
        min_party_size: 1,
        is_active: true,
      };

      await apiCentralized.createRestaurantConfig(configData);

      success = 'Configuración guardada exitosamente';

      // Cerrar modal después de 2 segundos
      setTimeout(() => {
        closeModal();
      }, 2000);
    } catch (err) {
      error = (err as Error).message || 'Error al guardar la configuración';
    } finally {
      isSubmitting = false;
    }
  }

  function updateDaySchedule(dayIndex: number, field: string, value: any): void {
    config.daysOfWeek[dayIndex][field] = value;
  }

  // Load configuration from API
  async function loadConfig(): Promise<void> {
    try {
      const activeConfig = await apiCentralized.getActiveRestaurantConfig();
      if (activeConfig) {
        config = {
          restaurantName: activeConfig.name || 'Mi Restaurante',
          maxCapacity: activeConfig.max_capacity || 50,
          openingTime: '08:00',
          closingTime: '22:00',
          averageTurnTime: activeConfig.time_slot_duration_minutes || 120,
          daysOfWeek: config.daysOfWeek, // Keep existing days structure
        };
      }
    } catch (err) {
      error = (err as Error).message || 'Error al cargar la configuración';
    }
  }

  // Listen for open configuration modal event
  onMount(() => {
    const openConfigHandler = () => {
      isOpen = true;
      loadConfig(); // Load config when modal opens
    };

    document.addEventListener('openConfigModal', openConfigHandler);

    return () => {
      document.removeEventListener('openConfigModal', openConfigHandler);
    };
  });
</script>

{#if isOpen}
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    onclick={handleBackdropClick}
    role="dialog"
    aria-modal="true"
    aria-labelledby="config-modal-title"
    tabindex="0"
    onkeydown={(e) => {
      if (e.key === 'Escape') closeModal();
    }}
  >
    <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 id="config-modal-title" class="text-2xl font-semibold text-slate-800">
            Configuración del Restaurante
          </h2>
          <button
            onclick={closeModal}
            class="text-slate-400 hover:text-slate-600 transition-colors"
            aria-label="Cerrar modal"
          >
            <span class="material-symbols-outlined text-2xl">close</span>
          </button>
        </div>

        {#if error}
          <div class="mb-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        {/if}

        {#if success}
          <div class="mb-4 p-3 bg-green-100 border border-green-200 text-green-700 rounded-lg">
            {success}
          </div>
        {/if}

        <form onsubmit={handleSave}>
          <!-- Información Básica -->
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-slate-700 mb-4">Información Básica</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="restaurantName" class="block text-sm font-medium text-slate-700 mb-1">
                  Nombre del Restaurante
                </label>
                <input
                  id="restaurantName"
                  type="text"
                  bind:value={config.restaurantName}
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="maxCapacity" class="block text-sm font-medium text-slate-700 mb-1">
                  Capacidad Máxima (personas)
                </label>
                <input
                  id="maxCapacity"
                  type="number"
                  bind:value={config.maxCapacity}
                  min="1"
                  max="500"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p class="text-xs text-slate-500 mt-1">Número máximo de personas simultáneas</p>
              </div>

              <div>
                <label for="openingTime" class="block text-sm font-medium text-slate-700 mb-1">
                  Hora de Apertura
                </label>
                <input
                  id="openingTime"
                  type="time"
                  bind:value={config.openingTime}
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label for="closingTime" class="block text-sm font-medium text-slate-700 mb-1">
                  Hora de Cierre
                </label>
                <input
                  id="closingTime"
                  type="time"
                  bind:value={config.closingTime}
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div class="md:col-span-2">
                <label for="averageTurnTime" class="block text-sm font-medium text-slate-700 mb-1">
                  Tiempo Promedio por Turno (minutos)
                </label>
                <input
                  id="averageTurnTime"
                  type="number"
                  bind:value={config.averageTurnTime}
                  min="30"
                  max="240"
                  step="15"
                  class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p class="text-xs text-slate-500 mt-1">
                  Tiempo promedio que ocupa una mesa (ej: 120 minutos = 2 horas)
                </p>
              </div>
            </div>
          </div>

          <!-- Horarios por Día -->
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-slate-700 mb-4">Horarios por Día</h3>
            <div class="space-y-3">
              {#each config.daysOfWeek as day, index}
                <div class="flex items-center gap-4 p-3 border border-slate-200 rounded-lg">
                  <div class="w-24">
                    <span class="font-medium text-slate-700">{day.name}</span>
                  </div>

                  <div class="flex items-center">
                    <input
                      type="checkbox"
                      bind:checked={day.isOpen}
                      class="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
                    />
                    <label class="ml-2 text-sm text-slate-600">Abierto</label>
                  </div>

                  {#if day.isOpen}
                    <div class="flex items-center gap-2">
                      <input
                        type="time"
                        bind:value={day.openTime}
                        class="px-2 py-1 border border-slate-300 rounded text-sm"
                      />
                      <span class="text-slate-500">a</span>
                      <input
                        type="time"
                        bind:value={day.closeTime}
                        class="px-2 py-1 border border-slate-300 rounded text-sm"
                      />
                    </div>
                  {:else}
                    <div class="text-sm text-slate-400">Cerrado</div>
                  {/if}
                </div>
              {/each}
            </div>
          </div>

          <!-- Resumen -->
          <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 class="font-semibold text-blue-900 mb-2">Resumen de Configuración</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span class="text-blue-700">Capacidad total:</span>
                <span class="font-medium text-blue-900 ml-1">{config.maxCapacity} personas</span>
              </div>
              <div>
                <span class="text-blue-700">Horario general:</span>
                <span class="font-medium text-blue-900 ml-1"
                  >{config.openingTime} - {config.closingTime}</span
                >
              </div>
              <div>
                <span class="text-blue-700">Turnos por día:</span>
                <span class="font-medium text-blue-900 ml-1">
                  {Math.floor(
                    (parseInt(config.closingTime.split(':')[0]) * 60 +
                      parseInt(config.closingTime.split(':')[1]) -
                      (parseInt(config.openingTime.split(':')[0]) * 60 +
                        parseInt(config.openingTime.split(':')[1]))) /
                      config.averageTurnTime,
                  )}
                </span>
              </div>
            </div>
          </div>

          <div class="flex gap-3">
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
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {isSubmitting ? 'Guardando...' : 'Guardar Configuración'}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
{/if}
