<script lang="ts">
  import { cn, createVariants } from "../../lib/utils";
  
  // Props
  export let variant: 'default' | 'destructive' = 'default';
  export let className = '';
  
  // Alert variants
  const alertVariants = createVariants(
    "relative w-full rounded-lg border px-4 py-3 text-sm grid has-[>svg]:grid-cols-[calc(var(--spacing)*4)_1fr] grid-cols-[0_1fr] has-[>svg]:gap-x-3 gap-y-0.5 items-start [&>svg]:size-4 [&>svg]:translate-y-0.5 [&>svg]:text-current",
    {
      variant: {
        default: "bg-card text-card-foreground",
        destructive: "text-destructive bg-card [&>svg]:text-current *:data-[slot=alert-description]:text-destructive/90"
      }
    },
    {
      variant: 'default'
    }
  );
  
  // Computed classes
  $: alertClass = cn(alertVariants({ variant, class: className }));
</script>

<div
  class={alertClass}
  role="alert"
  {...$$restProps}
>
  <slot />
</div>
