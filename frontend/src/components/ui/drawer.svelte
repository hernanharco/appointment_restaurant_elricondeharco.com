<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fade, fly } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  // PROPS
  export let open: boolean = false;
  export let className: string = "";
  export let title: string = "";
  export let description: string = "";
  export let direction: "bottom" | "right" | "left" | "top" = "bottom";

  function close() {
    open = false;
    dispatch("close");
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && open) close();
  }

  // Configuración de la animación según dirección
  const flyParams = {
    bottom: { y: 500, duration: 300 },
    top: { y: -500, duration: 300 },
    right: { x: 500, duration: 300 },
    left: { x: -500, duration: 300 }
  };

  // Clases dinámicas para la posición
  const positionClasses = {
    bottom: "inset-x-0 bottom-0 rounded-t-xl border-t max-h-[96%]",
    top: "inset-x-0 top-0 rounded-b-xl border-b max-h-[96%]",
    right: "inset-y-0 right-0 w-full sm:max-w-sm border-l h-full",
    left: "inset-y-0 left-0 w-full sm:max-w-sm border-r h-full"
  };
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-[2px]"
    transition:fade={{ duration: 200 }}
    on:click={close}
    on:keydown={handleKeydown}
  ></div>

  <div
    role="dialog"
    aria-modal="true"
    tabindex="0"
    transition:fly={flyParams[direction]}
    class={cn(
      "fixed z-50 flex flex-col bg-white shadow-2xl transition-all",
      positionClasses[direction],
      className
    )}
  >
    {#if direction === "bottom"}
      <div class="mx-auto mt-4 h-1.5 w-[50px] shrink-0 rounded-full bg-slate-200"></div>
    {/if}

    <div class="flex flex-col gap-1.5 p-6">
      {#if title}
        <h2 class="text-lg font-semibold leading-none tracking-tight">{title}</h2>
      {/if}
      {#if description}
        <p class="text-sm text-slate-500">{description}</p>
      {/if}
      <slot name="header" />
    </div>

    <div class="flex-1 overflow-y-auto px-6 pb-6">
      <slot />
    </div>

    {#if $$slots.footer}
      <div class="mt-auto flex flex-col gap-2 p-6 border-t">
        <slot name="footer" />
      </div>
    {/if}
  </div>
{/if}