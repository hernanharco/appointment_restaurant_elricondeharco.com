<script lang="ts">
  import { cn } from "../../lib/utils";
  
  export let className = '';
</script>

<div
  class={cn("flex flex-col gap-2 text-center sm:text-left", className)}
  role="heading"
  aria-level="2"
>
  <slot />
</div>
