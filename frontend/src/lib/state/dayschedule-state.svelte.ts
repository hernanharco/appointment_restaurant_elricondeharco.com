// src/lib/stores/app-config-state.svelte.ts
import { businessHoursApi } from '@/lib/api/business-hours';

class AppConfigState {
    openingRanges = $state<{ start: string, end: string }[]>([]);
    minHour = $state<number | null>(null);
    maxHour = $state<number | null>(null);
    isOpen = $state<boolean>(true);
    isLoading = $state<boolean>(false);

    // 🛡️ Guardias para evitar duplicados
    #lastDayFetched: number | null = null; // Quitamos $state porque no necesitamos que la UI reaccione a esto
    #abortController: AbortController | null = null;

    async fetchGlobalRange(dayOfWeek: number) {
        // 🎯 EXCELENCIA: Si el día solicitado es el mismo que ya cargamos, no hacemos nada
        // Esto resuelve el error "value is never read" [cite: 2026-02-18]
        if (dayOfWeek === this.#lastDayFetched && this.openingRanges.length > 0) {
            return;
        }

        // Cancelamos peticiones en vuelo
        if (this.#abortController) this.#abortController.abort();
        this.#abortController = new AbortController();

        this.isLoading = true;
        
        try {
            const data = await businessHoursApi.getGlobalRange(dayOfWeek);

            // Solo actualizamos si la carga fue exitosa
            this.openingRanges = data.ranges;
            this.isOpen = data.is_open;
            this.#lastDayFetched = dayOfWeek; // Ahora sí, el valor se "lee" arriba y se "escribe" aquí

            if (data.is_open) {
                this.minHour = parseInt(data.min_start.split(':')[0]);
                this.maxHour = parseInt(data.max_end.split(':')[0]);
            } else {
                this.minHour = null;
                this.maxHour = null;
            }
        } catch (error: any) {
            if (error.name !== 'AbortError') {
                console.error("❌ Error cargando rango global:", error);
                this.isOpen = false;
            }
        } finally {
            this.isLoading = false;
        }
    }

    get hoursList() {
        if (!this.isOpen || this.minHour === null || this.maxHour === null) return [];
        const length = this.maxHour - this.minHour + 1;
        return Array.from({ length }, (_, i) => i + (this.minHour as number));
    }
}

export const appConfigState = new AppConfigState();