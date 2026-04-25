<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fade, scale } from "svelte/transition";
  import { onMount } from "svelte";

  // PROPS
  export let className: string = "";

  // ESTADO
  let showMenu = false;
  let pos = { x: 0, y: 0 };
  let menuElement: HTMLElement;

  async function handleContextMenu(e: MouseEvent) {
    e.preventDefault();
    showMenu = false; // Reset si ya estaba abierto
    
    // Esperamos un tick para que se oculte y vuelva a aparecer en la nueva posición
    await new Promise(r => setTimeout(r, 0));
    
    pos = { x: e.clientX, y: e.clientY };
    showMenu = true;
  }

  function closeMenu() {
    showMenu = false;
  }

  // Cerrar al hacer clic fuera o redimensionar
  function handleOutsideClick(e: MouseEvent) {
    if (showMenu && menuElement && !menuElement.contains(e.target as Node)) {
      closeMenu();
    }
  }
</script>

<svelte:window on:click={handleOutsideClick} on:resize={closeMenu} on:scroll={closeMenu} />

<div 
  role="menu"
  tabindex="0"
  on:contextmenu={handleContextMenu}
  class={cn("w-full", className)}
>
  <slot name="trigger" />
</div>

{#if showMenu}
  <div
    bind:this={menuElement}
    transition:scale={{ duration: 100, start: 0.95 }}
    class={cn(
      "fixed z-50 min-w-[8rem] overflow-hidden rounded-md border bg-white p-1 shadow-md text-slate-950",
      className
    )}
    style="top: {pos.y}px; left: {pos.x}px;"
  >
    <slot />
  </div>
{/if}