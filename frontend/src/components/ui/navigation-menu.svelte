<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fly, fade } from "svelte/transition";
  import { ChevronDown } from "lucide-svelte";

  // PROPS
  export let className: string = "";

  // ESTADO: Maneja cuál menú está abierto (usando el nombre/id)
  let activeMenu: string | null = null;

  function toggleMenu(menu: string) {
    activeMenu = activeMenu === menu ? null : menu;
  }

  // Cerrar al hacer clic fuera
  function handleOutsideClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest('[data-slot="navigation-menu"]')) {
      activeMenu = null;
    }
  }
</script>

<svelte:window on:click={handleOutsideClick} />

<nav
  data-slot="navigation-menu"
  class={cn("relative z-10 flex max-w-max flex-1 items-center justify-center", className)}
>
  <ul class="group flex flex-1 list-none items-center justify-center gap-1">
    <slot {activeMenu} {toggleMenu} />
  </ul>
</nav>