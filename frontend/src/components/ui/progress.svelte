<script lang="ts">
  import { cn } from "../../lib/utils";
  import { tweened } from "svelte/motion";
  import { cubicOut } from "svelte/easing";

  // PROPS
  export let value: number = 0; // Valor de 0 a 100
  export let max: number = 100;
  export let className: string = "";

  // Animación fluida para el progreso
  const progressStore = tweened(0, {
    duration: 400,
    easing: cubicOut
  });

  // Cada vez que la prop 'value' cambie, el store se anima solo
  $: progressStore.set(value);
</script>

<div
  role="progressbar"
  aria-valuemin={0}
  aria-valuemax={max}
  aria-valuenow={value}
  data-slot="progress"
  class={cn(
    "relative h-2 w-full overflow-hidden rounded-full bg-slate-900/20",
    className
  )}
>
  <div
    data-slot="progress-indicator"
    class="h-full w-full flex-1 bg-slate-900 transition-all"
    style="transform: translateX(-{100 - ($progressStore / max) * 100}%);"
  ></div>
</div>