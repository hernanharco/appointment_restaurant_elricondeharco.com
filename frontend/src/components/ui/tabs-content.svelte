<script lang="ts">
  import { cn } from "../../lib/utils";
  import { getContext } from "svelte";
  
  // Props
  export let value: string;
  export let className = '';
  
  // Get tabs context
  const tabs = getContext('tabs') as any;
  
  // Computed classes
  $: contentClass = cn("flex-1 outline-none", className);
  $: isActive = tabs.value === value;
</script>

{#if isActive}
  <div
    class={contentClass}
    role="tabpanel"
    id={`panel-${value}`}
    aria-labelledby={`tab-${value}`}
    tabindex="0"
    {...$$restProps}
  >
    <slot />
  </div>
{/if}
