<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let className = '';
  
  // Generate initials from slot content
  function getInitials(): string {
    if (!$$slots.default) return '';
    // This is a simplified approach - in real usage, you might want to pass initials as a prop
    return '';
  }
  
  // Computed classes
  $: fallbackClass = cn(
    "bg-muted flex size-full items-center justify-center rounded-full text-sm font-medium",
    className
  );
  
  $: initials = getInitials();
</script>

<div class={fallbackClass} {...$$restProps}>
  {#if $$slots.default}
    <slot />
  {:else if initials}
    {initials}
  {:else}
    <svg class="size-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  {/if}
</div>
