<script lang="ts">
  import { cn } from "../../lib/utils";
  import { setContext } from "svelte";
  import { writable } from "svelte/store";

  export let className: string = "";

  // Este store guarda el ID del menú que está abierto actualmente
  const activeMenu = writable<string | null>(null);

  setContext("menubar", {
    activeMenu,
    toggle: (id: string) => {
      activeMenu.update(current => (current === id ? null : id));
    },
    open: (id: string) => {
      activeMenu.set(id);
    },
    close: () => {
      activeMenu.set(null);
    }
  });

  // Cerrar al hacer clic fuera
  function handleOutsideClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest('[data-slot="menubar"]')) {
      activeMenu.set(null);
    }
  }
</script>

<svelte:window on:click={handleOutsideClick} />

<nav
  data-slot="menubar"
  class={cn(
    "flex h-9 items-center gap-1 rounded-md border bg-white p-1 shadow-sm",
    className
  )}
>
  <slot />
</nav>