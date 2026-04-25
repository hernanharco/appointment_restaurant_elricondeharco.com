<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
  export let id = 'dialog-title';
</script>

<h2
  {id}
  class={cn("text-lg leading-none font-semibold", className)}
>
  <slot />
</h2>
