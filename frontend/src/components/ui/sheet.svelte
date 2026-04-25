<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, onMount } from 'svelte';
  import { X } from "lucide-svelte";
  
  // Props
  export let open = false;
  export let side: 'left' | 'right' | 'top' | 'bottom' = 'right';
  export let className = '';
  export let contentClassName = '';
  export let closeOnEscape = true;
  export let closeOnOverlayClick = true;
  
  const dispatch = createEventDispatcher();
  
  let sheetElement: HTMLDivElement;
  let overlayElement: HTMLDivElement;
  let previousFocus: HTMLElement | null = null;
  
  function close() {
    dispatch('close');
    open = false;
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && closeOnEscape) {
      event.preventDefault();
      close();
    }
  }
  
  function handleOverlayClick() {
    if (closeOnOverlayClick) {
      close();
    }
  }
  
  // Handle opening/closing
  $: if (open) {
    previousFocus = document.activeElement as HTMLElement;
    setTimeout(() => {
      sheetElement?.focus();
    }, 0);
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', handleKeydown);
  } else {
    document.body.style.overflow = '';
    setTimeout(() => {
      previousFocus?.focus();
    }, 0);
    document.removeEventListener('keydown', handleKeydown);
  }
  
  // Computed classes
  $: overlayClass = cn(
    "fixed inset-0 z-50 bg-black/50 transition-opacity duration-300",
    open ? "opacity-100" : "opacity-0 pointer-events-none"
  );
  
  $: sheetClass = cn(
    "fixed z-50 bg-background shadow-lg transition-transform duration-300",
    side === 'left' && "left-0 top-0 h-full w-80 border-r",
    side === 'right' && "right-0 top-0 h-full w-80 border-l",
    side === 'top' && "top-0 left-0 w-full h-80 border-b",
    side === 'bottom' && "bottom-0 left-0 w-full h-80 border-t",
    open && side === 'left' && "translate-x-0",
    open && side === 'right' && "translate-x-0",
    open && side === 'top' && "translate-y-0",
    open && side === 'bottom' && "translate-y-0",
    !open && side === 'left' && "-translate-x-full",
    !open && side === 'right' && "translate-x-full",
    !open && side === 'top' && "-translate-y-full",
    !open && side === 'bottom' && "translate-y-full",
    contentClassName,
    className
  );
</script>

{#if open}
  <div
    bind:this={overlayElement}
    class={overlayClass}
    onclick={handleOverlayClick}
    role="dialog"
    aria-modal="true"
  ></div>
  
  <div
    bind:this={sheetElement}
    class={sheetClass}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <button
      type="button"
      class="absolute top-4 right-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none"
      onclick={close}
      aria-label="Close sheet"
    >
      <X class="h-4 w-4" />
    </button>
    
    <div class="p-6">
      <slot />
    </div>
  </div>
{/if}
