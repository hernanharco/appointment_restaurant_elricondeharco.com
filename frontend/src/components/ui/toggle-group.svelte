<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, setContext } from 'svelte';
  
  // Props
  export let value: string | string[] = '';
  export let type: 'single' | 'multiple' = 'single';
  export let className = '';
  export let size: 'sm' | 'default' | 'lg' = 'default';
  
  const dispatch = createEventDispatcher();
  
  // Handle value changes
  function handleToggle(toggleValue: string) {
    if (type === 'single') {
      value = toggleValue;
    } else {
      const currentValues = Array.isArray(value) ? value : [];
      if (currentValues.includes(toggleValue)) {
        value = currentValues.filter(v => v !== toggleValue);
      } else {
        value = [...currentValues, toggleValue];
      }
    }
    dispatch('change', { value });
  }
  
  // Context for child items
  setContext('toggle-group', {
    value,
    type,
    size,
    handleToggle
  });
  
  // Computed classes
  $: groupClass = cn(
    "inline-flex items-center rounded-md",
    size === 'sm' && "h-8",
    size === 'default' && "h-9",
    size === 'lg' && "h-10",
    className
  );
</script>

<div class={groupClass} role="group" {...$$restProps}>
  <slot />
</div>
