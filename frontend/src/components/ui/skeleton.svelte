<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let className = '';
  export let width = '100%';
  export let height = '1.2rem';
  export let circle = false;
  export let lines = 1;
  
  // Computed classes
  $: skeletonClass = cn(
    "animate-pulse rounded-md bg-muted",
    circle ? "rounded-full" : "rounded-md",
    className
  );
  
  $: containerClass = cn("space-y-2");
</script>

{#if lines > 1}
  <div class={containerClass}>
    {#each Array(lines) as _, i}
      <div
        class={skeletonClass}
        style="width: {width}; height: {height}"
      ></div>
    {/each}
  </div>
{:else}
  <div
    class={skeletonClass}
    style="width: {width}; height: {height}"
  ></div>
{/if}
