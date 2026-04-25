<script lang="ts">
  import { cn } from "../../lib/utils";
  import { X } from "lucide-svelte";
  import { onMount } from "svelte";
  
  // Svelte 5 Props con Runes
  let { 
    open = $bindable(false), 
    children,
    class: className = '',
    overlayClassName = '',
    closeOnEscape = true,
    closeOnOverlayClick = true
  } = $props();
  
  let dialogElement = $state<HTMLDivElement | null>(null);
  let overlayElement = $state<HTMLDivElement | null>(null);
  let previousFocus = $state<HTMLElement | null>(null);

  // Esta función solo se ejecuta en el NAVEGADOR cuando 'open' cambia
  $effect(() => {
    if (typeof document === 'undefined') return;

    if (open) {
      previousFocus = document.activeElement as HTMLElement;
      // Bloquear scroll
      const originalOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      
      // Enfocar el diálogo después de que se dibuje
      setTimeout(() => dialogElement?.focus(), 0);

      // Limpieza cuando el efecto se destruye o el modal se cierra
      return () => {
        document.body.style.overflow = originalOverflow;
        previousFocus?.focus();
      };
    }
  });

  function close() {
    open = false;
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && closeOnEscape) {
      event.preventDefault();
      close();
    }
    // Lógica de Trap Focus simplificada para Svelte 5
    if (event.key === 'Tab' && dialogElement) {
      const focusable = dialogElement.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusable.length === 0) return;
      
      const first = focusable[0] as HTMLElement;
      const last = focusable[focusable.length - 1] as HTMLElement;

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }

  // Escuchar teclado solo en el navegador
  $effect(() => {
    if (open) {
      window.addEventListener('keydown', handleKeydown);
      return () => window.removeEventListener('keydown', handleKeydown);
    }
  });
</script>

{#if open}
  <div
    bind:this={overlayElement}
    class={cn(
      "fixed inset-0 z-50 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200",
      overlayClassName
    )}
    onclick={() => closeOnOverlayClick && close()}
    role="presentation"
  ></div>

  <div
    bind:this={dialogElement}
    class={cn(
      "fixed top-[50%] left-[50%] z-50 grid w-full max-w-[calc(100%-2rem)] translate-x-[-50%] translate-y-[-50%] gap-4 rounded-lg border bg-white p-6 shadow-lg animate-in zoom-in-95 duration-200 sm:max-w-lg",
      className
    )}
    tabindex="-1"
    role="dialog"
    aria-modal="true"
  >
    {@render children?.()}

    <button
      type="button"
      class="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:pointer-events-none"
      onclick={close}
      aria-label="Close dialog"
    >
      <X class="size-4" />
    </button>
  </div>
{/if}