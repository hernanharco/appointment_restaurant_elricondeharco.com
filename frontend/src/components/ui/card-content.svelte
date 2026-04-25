<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn("px-6 last:pb-6", className)}
  {...$$restProps}
>
  <slot />
</div>
