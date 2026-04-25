<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fade, scale } from "svelte/transition";
  import { setContext, createEventDispatcher } from "svelte";
  import { writable } from "svelte/store";

  // PROPS
  export let className: string = "";
  export let open: boolean = false;
  export let align: "left" | "right" = "left";

  const dispatch = createEventDispatcher();
  const openStore = writable(open);

  // Actualizar store cuando cambie la prop
  $: openStore.set(open);
  
  // Notificar al padre cuando cambie el estado internamente
  $: dispatch("openChange", $openStore);

  setContext("dropdown", {
    open: openStore,
    close: () => {
      open = false;
      openStore.set(false);
    }
  });

  // Acción para cerrar al hacer clic fuera
  function clickOutside(node: HTMLElement) {
    const handleClick = (event: MouseEvent) => {
      if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
        open = false;
        openStore.set(false);
      }
    };

    document.addEventListener("click", handleClick, true);
    return {
      destroy() {
        document.removeEventListener("click", handleClick, true);
      }
    };
  }

  function toggle() {
    open = !open;
    openStore.set(open);
  }
</script>

<div class="relative inline-block" use:clickOutside>
  <div 
    role="button" 
    tabindex="0" 
    on:click={toggle}
    on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggle()}
    aria-haspopup="true"
    aria-expanded={$openStore}
  >
    <slot name="trigger" />
  </div>

  {#if $openStore}
    <div
      transition:scale={{ duration: 150, start: 0.95, opacity: 0 }}
      class={cn(
        "absolute z-50 min-w-32 mt-2 rounded-md border bg-white p-1 shadow-md text-slate-950 origin-top-left",
        align === "right" ? "right-0" : "left-0",
        className
      )}
    >
      <slot />
    </div>
  {/if}
</div>