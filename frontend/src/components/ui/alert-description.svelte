<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn(
    "text-muted-foreground col-start-2 grid justify-items-start gap-1 text-sm [&_p]:leading-relaxed",
    className
  )}
  {...$$restProps}
>
  <slot />
</div>
