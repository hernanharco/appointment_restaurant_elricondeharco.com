<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, onMount, setContext } from "svelte";
  
  // Props
  export let value = '';
  export let className = '';
  export let orientation: 'horizontal' | 'vertical' = 'horizontal';
  export let activationMode: 'automatic' | 'manual' = 'automatic';
  
  const dispatch = createEventDispatcher();
  
  // Context for child components
  setContext('tabs', {
    value,
    orientation,
    activationMode,
    registerTab: (tabValue: string) => {},
    unregisterTab: (tabValue: string) => {},
    selectTab: (tabValue: string) => {
      value = tabValue;
      dispatch('change', { value: tabValue });
    }
  });
  
  let tabs = new Set<string>();
  
  // Computed classes
  $: tabsClass = cn("flex flex-col gap-2", className);
</script>

<div class={tabsClass} {...$$restProps}>
  <slot />
</div>
