<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<p
  class={cn("text-muted-foreground", className)}
  {...$$restProps}
>
  <slot />
</p>
