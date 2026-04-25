<script lang="ts">
  import { cn } from "../../lib/utils";

  // Agregamos for = undefined para que sea opcional
  let { class: className = '', children, for: forId = undefined, ...rest } = $props();
</script>

<label
  for={forId}
  class={cn(
    "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-slate-700",
    className
  )}
  {...rest}
>
  {@render children?.()}
</label>