<script lang="ts">
  import { cn } from "../../lib/utils";
  import { scale } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  // PROPS
  export let className: string = "";
  export let open: boolean = false;
  export let align: "left" | "right" | "center" = "center";

  const dispatch = createEventDispatcher();

  // Acción para cerrar al hacer clic fuera del elemento
  function clickOutside(node: HTMLElement) {
    const handleClick = (event: MouseEvent) => {
      if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
        open = false;
        dispatch("openChange", open);
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
    dispatch("openChange", open);
  }

  // Lógica de alineación para las clases de Tailwind
  const alignClasses = {
    left: "left-0",
    right: "right-0",
    center: "left-1/2 -translate-x-1/2"
  };
</script>

<div class="relative inline-block" use:clickOutside>
  <div 
    role="button" 
    tabindex="0" 
    on:click={toggle}
    on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggle()}
    class="cursor-pointer"
  >
    <slot name="trigger" />
  </div>

  {#if open}
    <div
      transition:scale={{ duration: 150, start: 0.95, opacity: 0 }}
      class={cn(
        "absolute z-50 mt-2 w-72 rounded-md border bg-white p-4 shadow-md outline-none origin-top",
        alignClasses[align],
        className
      )}
      data-slot="popover-content"
    >
      <slot />
    </div>
  {/if}
</div>