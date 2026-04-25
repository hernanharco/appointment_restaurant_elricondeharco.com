<script lang="ts">
  import { cn } from "../../lib/utils";
  import { getContext } from "svelte";
  
  // Props
  export let value: string;
  export let disabled = false;
  export let className = '';
  
  // Get tabs context
  const tabs = getContext('tabs') as any;
  
  function handleClick() {
    if (!disabled) {
      tabs.selectTab(value);
    }
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (disabled) return;
    
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }
  }
  
  // Computed classes
  $: triggerClass = cn(
    "inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-xl border border-transparent px-2 py-1 text-sm font-medium whitespace-nowrap transition-[color,box-shadow] focus-visible:ring-[3px] focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
    "text-foreground dark:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:outline-ring",
    tabs.value === value 
      ? "bg-card dark:text-foreground dark:border-input dark:bg-input/30" 
      : "dark:data-[state=active]:border-input dark:data-[state=active]:bg-input/30",
    disabled && "opacity-50 cursor-not-allowed",
    className
  );
</script>

<button
  type="button"
  class={triggerClass}
  role="tab"
  aria-selected={tabs.value === value}
  aria-controls={`panel-${value}`}
  tabindex={tabs.value === value ? 0 : -1}
  {disabled}
  onclick={handleClick}
  onkeydown={handleKeydown}
  {...$$restProps}
>
  <slot />
</button>
