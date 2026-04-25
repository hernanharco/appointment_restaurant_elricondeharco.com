<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
  export let id = 'dialog-description';
</script>

<p
  {id}
  class={cn("text-muted-foreground text-sm", className)}
>
  <slot />
</p>
