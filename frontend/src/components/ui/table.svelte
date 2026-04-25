<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let className = '';
  
  // Computed classes
  $: tableClass = cn(
    "w-full caption-bottom text-sm",
    className
  );
</script>

<table class={tableClass} {...$$restProps}>
  <slot />
</table>
