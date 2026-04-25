import { healthApi } from '@/lib/api/health';

/**
 * STORE DE ESTADO DE SALUD (Health System)
 * ---------------------------------------
 * Este orquestador se encarga de gestionar la percepción del frontend 
 * sobre la disponibilidad del backend (FastAPI).
 * * Principio SRP: Su única responsabilidad es saber si el servidor responde.
 */
class HealthStore {
  // 🔒 CAMPOS PRIVADOS (#)
  // Usamos '#' para que nadie fuera de esta clase pueda alterar el estado directamente.
  // Solo la lógica interna de checkHealth() puede decidir si estamos Online u Offline.
  
  // $state: Rune de Svelte 5 que hace que cualquier componente que use esta variable
  // se actualice automáticamente cuando su valor cambie.
  #isOnline = $state(true);
  #isChecking = $state(false);

  // 📖 GETTERS (Solo lectura)
  // Permiten que los componentes lean el valor pero no lo modifiquen.
  // Ejemplo de uso: if (healthStore.isOnline) { ... }
  get isOnline() { return this.#isOnline; }
  get isChecking() { return this.#isChecking; }

  constructor() {
    // Verificamos 'window' para asegurarnos de que el código corre en el navegador 
    // y no durante el renderizado estático de Astro (SSR).
    if (typeof window !== 'undefined') {
      this.checkHealth(); // Ejecuta una comprobación inicial al cargar la web.
    }
  }

  /**
   * LÓGICA DE VERIFICACIÓN
   * ----------------------
   * Se comunica con el backend a través de la capa de API.
   * Maneja el estado de carga y las posibles excepciones.
   */
  async checkHealth() {
    // "Guard Clause": Si ya hay un chequeo en curso, no disparamos otro.
    // Esto ahorra recursos y evita colisiones de red.
    if (this.#isChecking) return;

    this.#isChecking = true; // Iniciamos estado de "Cargando..."
    
    try {
      // Intentamos comunicarnos con el endpoint /health definido en healthApi.
      // Si el backend responde (status 200), asumimos que todo está OK.
      await healthApi.checkStatus();
      this.#isOnline = true;
    } catch (error) {
      // Si el fetch falla (backend apagado, error de red, timeout), 
      // marcamos el estado como Offline.
      this.#isOnline = false;
      console.warn("[HealthStore] El servidor no responde.");
    } finally {
      // 'finally' se ejecuta SIEMPRE, haya error o no.
      // Ideal para apagar indicadores de carga (spinners).
      this.#isChecking = false;
    }
  }
}

/**
 * PATRÓN SINGLETON
 * ----------------
 * Exportamos una única instancia de la clase. 
 * Esto garantiza que toda la aplicación use el mismo estado de salud.
 */
export const healthStore = new HealthStore();