<script lang="ts">
  import { cn } from "../../lib/utils";

  // En Svelte 5 definimos las props así para tener mejor autocompletado
  let { class: className = '', children, ...rest } = $props();
</script>

<div
  class={cn(
    "bg-card text-card-foreground flex flex-col gap-6 rounded-xl border shadow-sm",
    className
  )}
  {...rest}
>
  {@render children?.()}
</div>