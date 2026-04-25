<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, onMount } from 'svelte';
  
  // Props
  export let open = false;
  export let content = '';
  export let placement: 'top' | 'bottom' | 'left' | 'right' = 'top';
  export let delay = 0;
  export let className = '';
  export let contentClassName = '';
  
  const dispatch = createEventDispatcher();
  
  let triggerElement: HTMLElement;
  let tooltipElement: HTMLDivElement;
  let timeoutId: number;
  
  function showTooltip() {
    if (timeoutId) clearTimeout(timeoutId);
    
    if (delay > 0) {
      timeoutId = setTimeout(() => {
        open = true;
      }, delay);
    } else {
      open = true;
    }
  }
  
  function hideTooltip() {
    if (timeoutId) clearTimeout(timeoutId);
    open = false;
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      hideTooltip();
    }
  }
  
  onMount(() => {
    document.addEventListener('keydown', handleKeydown);
    return () => {
      document.removeEventListener('keydown', handleKeydown);
    };
  });
  
  // Computed classes
  $: triggerClass = cn("inline-flex", className);
  
  $: tooltipClass = cn(
    "absolute z-50 px-2 py-1 text-xs text-primary-foreground bg-primary rounded-md shadow-md pointer-events-none transition-opacity duration-200",
    open ? "opacity-100" : "opacity-0",
    contentClassName
  );
  
  // Position styles
  $: positionStyles = {
    top: placement === 'top' ? '100%' : placement === 'bottom' ? 'auto' : '50%',
    bottom: placement === 'bottom' ? '100%' : 'auto',
    left: placement === 'left' ? '100%' : placement === 'right' ? 'auto' : '50%',
    right: placement === 'right' ? '100%' : 'auto',
    transform: placement === 'top' ? 'translate(-50%, 0.5rem)' : 
               placement === 'bottom' ? 'translate(-50%, -0.5rem)' :
               placement === 'left' ? 'translate(-0.5rem, -50%)' :
               'translate(0.5rem, -50%)'
  };
</script>

<div class="relative inline-block">
  <div
    bind:this={triggerElement}
    class={triggerClass}
    on:mouseenter={showTooltip}
    on:mouseleave={hideTooltip}
    on:focus={showTooltip}
    on:blur={hideTooltip}
    role="button"
    tabindex="0"
    aria-describedby="tooltip"
    {...$$restProps}
  >
    <slot />
  </div>
  
  {#if open && content}
    <div
      bind:this={tooltipElement}
      class={tooltipClass}
      id="tooltip"
      role="tooltip"
      style={positionStyles}
    >
      {content}
    </div>
  {/if}
</div>
