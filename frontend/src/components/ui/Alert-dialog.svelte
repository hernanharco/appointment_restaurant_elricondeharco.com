<script lang="ts">
  import { cn } from "../../lib/utils";
  import { fade, scale } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let open: boolean = false;
  export let className: string = "";
  export let title: string = "";
  export let description: string = "";

  function close() {
    open = false;
    dispatch("close");
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && open) close();
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div
    class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
    transition:fade={{ duration: 150 }}
    on:click={close}
    on:keydown={(e) => e.key === 'Enter' && close()}
    role="button"
    tabindex="0"
    aria-label="Cerrar modal"
  ></div>

  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
    <div
      role="alertdialog"
      aria-modal="true"
      transition:scale={{ duration: 200, start: 0.95 }}
      class={cn(
        "bg-white w-full max-w-lg p-6 rounded-lg border shadow-lg pointer-events-auto",
        className
      )}
    >
      <div class="flex flex-col gap-2 text-center sm:text-left">
        {#if title}
          <h2 class="text-lg font-semibold">{title}</h2>
        {/if}
        {#if description}
          <p class="text-sm text-slate-500">{description}</p>
        {/if}
        <slot name="header" />
      </div>

      <div class="py-4">
        <slot />
      </div>

      <div class="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-4">
        <slot name="footer" />
      </div>
    </div>
  </div>
{/if}