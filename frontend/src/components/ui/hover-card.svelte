<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fade, scale } from "svelte/transition";

  // PROPS
  export let className: string = "";
  export let openDelay: number = 700;
  export let closeDelay: number = 300;

  // ESTADO
  let isHovered = false;
  let timeout: ReturnType<typeof setTimeout>;

  function handleEnter() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      isHovered = true;
    }, openDelay);
  }

  function handleLeave() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      isHovered = false;
    }, closeDelay);
  }
</script>

<div 
  class="relative inline-block"
  on:mouseenter={handleEnter}
  on:mouseleave={handleLeave}
  role="button"
  tabindex="0"
>
  <div data-slot="hover-card-trigger">
    <slot name="trigger" />
  </div>

  {#if isHovered}
    <div
      transition:scale={{ duration: 150, start: 0.95, opacity: 0 }}
      class={cn(
        "absolute z-50 w-64 rounded-md border bg-white p-4 shadow-md outline-none",
        "bottom-full left-1/2 -translate-x-1/2 mb-2", // Posición por defecto: arriba centrado
        className
      )}
      data-slot="hover-card-content"
    >
      <slot />
    </div>
  {/if}
</div>