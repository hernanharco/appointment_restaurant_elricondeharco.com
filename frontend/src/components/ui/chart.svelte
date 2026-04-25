<script lang="ts">
  import { setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { cn } from "../../lib/utils";

  // PROPS
  export let config: Record<string, { label?: string; color?: string; theme?: Record<string, string> }> = {};
  export let className: string = "";
  export let id: string = `chart-${Math.random().toString(36).substring(2, 9)}`;

  // Crear el CSS dinámico para los colores del gráfico
  $: chartStyle = Object.entries(config)
    .map(([key, item]) => {
      const color = item.color || (item.theme ? item.theme.light : "");
      return color ? `--color-${key}: ${color};` : "";
    })
    .join(" ");

  // Proveer la configuración a componentes hijos (Tooltip, Legend)
  const configStore = writable(config);
  $: configStore.set(config);
  setContext('chart-config', configStore);
</script>

<div
  {id}
  data-slot="chart"
  class={cn(
    "flex aspect-video justify-center text-xs",
    // Estilos para inyectar en las librerías de gráficas
    "[&_.recharts-cartesian-axis-tick_text]:fill-slate-500",
    "[&_.recharts-cartesian-grid_line]:stroke-slate-200",
    "[&_.recharts-curve.recharts-tooltip-cursor]:stroke-slate-200",
    className
  )}
  style={chartStyle}
>
  <slot />
</div>

<style>
  /* Aquí puedes añadir animaciones globales para tus gráficas */
  :global(.recharts-surface) {
    overflow: visible;
  }
</style>