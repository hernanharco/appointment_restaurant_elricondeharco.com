<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let orientation: 'horizontal' | 'vertical' = 'horizontal';
  export let decorative = true;
  export let className = '';
  
  // Computed classes
  $: separatorClass = cn(
    "bg-border shrink-0",
    orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
    className
  );
</script>

<div
  class={separatorClass}
  role={decorative ? 'none' : 'separator'}
  aria-orientation={decorative ? undefined : orientation}
  {...$$restProps}
></div>
