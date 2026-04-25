<script lang="ts">
  import { cn } from "../../lib/utils";
  import { getContext } from 'svelte';
  
  // Props
  export let value: string;
  export let disabled = false;
  export let className = '';
  export let pressed = false;
  
  // Get toggle group context
  const toggleGroup = getContext('toggle-group') as any;
  
  function handleClick() {
    if (disabled) return;
    
    if (toggleGroup) {
      toggleGroup.handleToggle(value);
    } else {
      pressed = !pressed;
    }
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (disabled) return;
    
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }
  }
  
  // Computed state
  $: isActive = toggleGroup 
    ? (toggleGroup.type === 'single' ? toggleGroup.value === value : 
       Array.isArray(toggleGroup.value) && toggleGroup.value.includes(value))
    : pressed;
  
  // Computed classes
  $: toggleClass = cn(
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    toggleGroup?.size === 'sm' && "h-8 px-3",
    toggleGroup?.size === 'default' && "h-9 px-3",
    toggleGroup?.size === 'lg' && "h-10 px-3",
    !toggleGroup && "h-9 px-3",
    isActive 
      ? "bg-primary text-primary-foreground hover:bg-primary/90" 
      : "bg-transparent text-muted-foreground hover:bg-muted hover:text-foreground",
    className
  );
</script>

<button
  type="button"
  class={toggleClass}
  {disabled}
  aria-pressed={isActive}
  onclick={handleClick}
  onkeydown={handleKeydown}
  role="button"
  {...$$restProps}
>
  <slot />
</button>
