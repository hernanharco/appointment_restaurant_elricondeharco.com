<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<h4
  class={cn("leading-none", className)}
  {...$$restProps}
>
  <slot />
</h4>
