<script lang="ts">
  import { cn } from "../../lib/utils";
  import { ChevronRight, MoreHorizontal } from "lucide-svelte";

  // Props del contenedor principal
  export let className: string = "";
</script>

<nav aria-label="breadcrumb" data-slot="breadcrumb" class={cn("relative", className)}>
  <ol
    data-slot="breadcrumb-list"
    class="text-muted-foreground flex flex-wrap items-center gap-1.5 text-sm break-words sm:gap-2.5"
  >
    <slot />
  </ol>
</nav>

<style>
  :global([data-slot="breadcrumb-item"]) {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
  }

  :global([data-slot="breadcrumb-link"]) {
    transition-property: color;
    transition-duration: 200ms;
  }

  :global([data-slot="breadcrumb-link"]:hover) {
    color: var(--foreground, #0f172a);
  }

  :global([data-slot="breadcrumb-page"]) {
    font-weight: 400;
    color: var(--foreground, #0f172a);
  }

  :global([data-slot="breadcrumb-separator"] svg) {
    width: 0.875rem;
    height: 0.875rem;
  }
</style>