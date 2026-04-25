<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, } from 'svelte';
  import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from "lucide-svelte";
  
  // Props
  export let open = false;
  export let message = '';
  export let type: 'default' | 'success' | 'error' | 'info' | 'warning' = 'default';
  export let duration = 5000;
  export let position: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center' = 'top-right';
  export let action: { label: string; handler: () => void } | undefined = undefined;
  
  const dispatch = createEventDispatcher();
  
  let timeoutId: number;
  
  // Auto-dismiss
  $: if (open && duration > 0) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      close();
    }, duration);
  }
  
  function close() {
    open = false;
    dispatch('close');
  }
  
  // Icon mapping
  const icons = {
    default: Info,
    success: CheckCircle,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info
  };
  
  // Computed classes
  $: toastClass = cn(
    "fixed z-50 flex items-center gap-3 p-4 rounded-lg border shadow-lg max-w-sm transition-all duration-300 transform",
    position.includes('top') ? "top-4" : "bottom-4",
    position.includes('right') ? "right-4" : position.includes('left') ? "left-4" : "left-1/2 -translate-x-1/2",
    position.includes('center') && "left-1/2 -translate-x-1/2",
    open ? "translate-y-0 opacity-100" : "translate-y-full opacity-0 pointer-events-none",
    type === 'default' && "bg-background text-foreground border-border",
    type === 'success' && "bg-green-50 text-green-800 border-green-200 dark:bg-green-900/20 dark:text-green-200 dark:border-green-800",
    type === 'error' && "bg-red-50 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-200 dark:border-red-800",
    type === 'warning' && "bg-yellow-50 text-yellow-800 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-200 dark:border-yellow-800",
    type === 'info' && "bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-900/20 dark:text-blue-200 dark:border-blue-800"
  );
  
  $: iconClass = cn(
    "flex-shrink-0",
    type === 'success' && "text-green-600 dark:text-green-400",
    type === 'error' && "text-red-600 dark:text-red-400",
    type === 'warning' && "text-yellow-600 dark:text-yellow-400",
    type === 'info' && "text-blue-600 dark:text-blue-400"
  );
  
  $: CurrentIcon = icons[type];
</script>

{#if open}
  <div class={toastClass} role="alert" aria-live="polite">
    <CurrentIcon class={iconClass} />
    
    <div class="flex-1">
      <p class="text-sm font-medium">{message}</p>
      {#if action}
        <button
          type="button"
          class="mt-2 text-sm font-medium underline hover:no-underline focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 rounded"
          onclick={() => {
            action.handler();
            close();
          }}
        >
          {action.label}
        </button>
      {/if}
    </div>
    
    <button
      type="button"
      class="shrink-0 p-1 rounded-md hover:bg-black/10 dark:hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
      onclick={close}
      aria-label="Close notification"
    >
      <X class="h-4 w-4" />
    </button>
  </div>
{/if}
