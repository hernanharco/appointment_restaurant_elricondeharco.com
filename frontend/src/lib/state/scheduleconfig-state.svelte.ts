/**
 * scheduleconfig-state.svelte.ts
 * Responsabilidad: Gestionar el estado de edición de horarios de un colaborador.
 * Stack: Svelte 5 (Runes).
 */
import { businessHoursApi } from '@/lib/api/business-hours';
import { toastStore } from '@/lib/state/toast-state.svelte';
import { DAYS_LABELS } from '@/lib/constants/days';

export class ScheduleConfigStore {
  // --- Estados Reactivos ---
  config = $state<Record<number, any>>({});
  isLoading = $state(false);
  isSaving = $state(false);

  // --- Propiedades Derivadas ---
  isConfigEmpty = $derived(
    Object.values(this.config).every((day: any) => !day?.is_enabled)
  );

  /**
   * Carga la configuración desde la API y la formatea para el componente
   */
  async load(collaboratorId: number) {
    this.isLoading = true;
    this.config = {}; // Limpiar anterior

    try {
      const data = await businessHoursApi.getWeeklyConfig(collaboratorId);
      
      // Inicializar todos los días basados en nuestras constantes
      const newConfig: Record<number, any> = {};
      
      DAYS_LABELS.forEach(label => {
        // Buscamos si el día ya existe en la DB
        const dbDay = data.find((d: any) => d.day_of_week === label.id);
        
        if (dbDay) {
          newConfig[label.id] = {
            ...dbDay,
            // Aseguramos que los slots tengan el formato correcto
            time_slots: dbDay.time_slots.map((s: any) => ({
              start_time: s.start_time,
              end_time: s.end_time,
              slot_order: s.slot_order
            }))
          };
        } else {
          // Día vacío por defecto
          newConfig[label.id] = {
            day_of_week: label.id,
            day_name: label.name,
            is_enabled: false,
            is_split_shift: false,
            time_slots: []
          };
        }
      });

      this.config = newConfig;
    } catch (error) {
      toastStore.show('Error al cargar el horario', 'error');
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Toggles (activar/desactivar) un día
   */
  toggleDay(dayId: number) {
    const day = this.config[dayId];
    day.is_enabled = !day.is_enabled;
    
    if (day.is_enabled && day.time_slots.length === 0) {
      day.time_slots = [{ start_time: '09:00', end_time: '18:00', slot_order: 1 }];
    }
  }

  /**
   * Maneja el cambio de jornada partida
   */
  toggleSplitTurn(dayId: number) {
    const day = this.config[dayId];
    if (!day.is_enabled) return;

    day.is_split_shift = !day.is_split_shift;
    day.time_slots = day.is_split_shift
      ? [
          { start_time: '09:00', end_time: '13:00', slot_order: 1 },
          { start_time: '16:00', end_time: '20:00', slot_order: 2 },
        ]
      : [{ start_time: '09:00', end_time: '18:00', slot_order: 1 }];
  }

  /**
   * Guarda los cambios usando el endpoint Bulk
   */
  async save(collaboratorId: number, onComplete: () => void) {
    this.isSaving = true;
    try {
      await businessHoursApi.updateBulkConfig(collaboratorId, $state.snapshot(this.config));
      toastStore.show('Horario guardado con éxito', 'success');
      onComplete();
    } catch (error) {
      toastStore.show('Error al guardar los cambios', 'error');
    } finally {
      this.isSaving = false;
    }
  }
}

export const scheduleConfigStore = new ScheduleConfigStore();