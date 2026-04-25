<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn("flex items-center px-6 pb-6 [.border-t]:pt-6", className)}
  {...$$restProps}
>
  <slot />
</div>
