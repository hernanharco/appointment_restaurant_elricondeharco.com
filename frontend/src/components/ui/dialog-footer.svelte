<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end", className)}
>
  <slot />
</div>
