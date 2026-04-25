<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let src = '';
  export let alt = '';
  export let className = '';
  
  // Handle image load error
  function handleError(event: Event) {
    const target = event.target as HTMLImageElement;
    target.style.display = 'none';
    const fallback = target.nextElementSibling as HTMLElement;
    if (fallback) {
      fallback.style.display = 'flex';
    }
  }
  
  // Computed classes
  $: imageClass = cn("aspect-square size-full", className);
</script>

<div class="relative size-full">
  <img
    {src}
    {alt}
    class={imageClass}
    on:error={handleError}
    {...$$restProps}
  />
  <slot name="fallback" />
</div>
