<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn(
    "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 pt-6 has-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
    className
  )}
  {...$$restProps}
>
  <slot />
</div>
