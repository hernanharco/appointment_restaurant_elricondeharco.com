<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let className = '';
  export let side: 'left' | 'right' = 'left';
  export let collapsible = true;
  export let defaultCollapsed = false;
  
  let collapsed = defaultCollapsed;
  
  function toggle() {
    if (collapsible) {
      collapsed = !collapsed;
    }
  }
  
  // Computed classes
  $: sidebarClass = cn(
    "flex h-full bg-background border-r transition-all duration-300",
    side === 'left' ? "flex-row" : "flex-row-reverse",
    collapsed ? "w-16" : "w-64",
    className
  );
  
  $: contentClass = cn(
    "flex-1 overflow-hidden",
    collapsed ? "ml-0" : side === 'left' ? "ml-64" : "mr-64"
  );
</script>

<div class="flex h-full">
  <aside class={sidebarClass} {...$$restProps}>
    {#if collapsible}
      <button
        type="button"
        class="absolute -right-3 top-6 z-10 h-6 w-6 rounded-full bg-background border shadow-md flex items-center justify-center"
        onclick={toggle}
        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        <svg
          class="h-4 w-4 transition-transform"
          class:rotate-180={side === 'right'}
          class:rotate-180={!collapsed && side === 'left'}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
    {/if}
    
    <div class="flex flex-col h-full">
      <slot />
    </div>
  </aside>
  
  <main class={contentClass}>
    <slot name="content" />
  </main>
</div>
