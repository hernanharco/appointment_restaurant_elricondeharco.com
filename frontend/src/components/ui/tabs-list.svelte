<script lang="ts">
  import { cn } from "../../lib/utils";
  import { getContext } from "svelte";
  
  // Props
  export let className = '';
  
  // Get tabs context
  const tabs = getContext('tabs') as any;
  
  // Computed classes
  $: listClass = cn(
    "bg-muted text-muted-foreground h-9 w-fit items-center justify-center rounded-xl p-[3px] flex",
    tabs.orientation === 'vertical' ? "flex-col" : "",
    className
  );
</script>

<div
  class={listClass}
  role="tablist"
  aria-orientation={tabs.orientation}
  {...$$restProps}
>
  <slot />
</div>
