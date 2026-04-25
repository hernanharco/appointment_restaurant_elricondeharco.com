<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let ratio: number | string = 16 / 9;
  export let className = '';
  
  // Convert ratio to CSS custom property
  $: ratioValue = typeof ratio === 'number' ? ratio : parseFloat(ratio);
  $: paddingBottom = (1 / ratioValue) * 100;
</script>

<div
  class={cn("relative w-full", className)}
  style="padding-bottom: {paddingBottom}%"
  {...$$restProps}
>
  <div class="absolute inset-0">
    <slot />
  </div>
</div>
