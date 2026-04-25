<script lang="ts">
  import { cn } from "../../lib/utils";
  import { slide } from "svelte/transition";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  // PROPS
  export let open: boolean = false;
  export let className: string = "";

  function toggle() {
    open = !open;
    dispatch("change", open);
  }
</script>

<div class={cn("w-full", className)} data-slot="collapsible">
  <div 
    role="button" 
    tabindex="0"
    on:click={toggle}
    on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggle()}
    class="cursor-pointer"
    data-slot="collapsible-trigger"
    aria-expanded={open}
  >
    <slot name="trigger" {open} />
  </div>

  {#if open}
    <div 
      transition:slide={{ duration: 200 }} 
      data-slot="collapsible-content"
    >
      <slot />
    </div>
  {/if}
</div>