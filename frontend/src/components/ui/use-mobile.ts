// src/lib/hooks/useIsMobile.svelte.ts
const MOBILE_BREAKPOINT = 768;

export function useIsMobile() {
  // Creamos un estado reactivo
  let isMobile = $state(false);

  // En Svelte, esto se ejecuta al montar el componente
  $effect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);
    
    const onChange = () => {
      isMobile = window.innerWidth < MOBILE_BREAKPOINT;
    };

    mql.addEventListener("change", onChange);
    // Ejecutamos una vez al inicio
    onChange();

    // La función que retornamos es la limpieza (cleanup)
    return () => mql.removeEventListener("change", onChange);
  });

  // Retornamos un objeto o una función para mantener la reactividad
  return {
    get current() { return isMobile }
  };
}