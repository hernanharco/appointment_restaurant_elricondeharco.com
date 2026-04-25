<script lang="ts">
  import { cn } from "../../lib/utils";
  import { onMount, onDestroy } from "svelte";
  
  // Props
  export let className = '';
  export let orientation: 'horizontal' | 'vertical' = 'vertical';
  
  let scrollElement: HTMLDivElement;
  let scrollContent: HTMLDivElement;
  let scrollThumb: HTMLDivElement;
  let scrollTrack: HTMLDivElement;
  
  let isScrolling = false;
  let isDragging = false;
  let startY = 0;
  let scrollTop = 0;
  
  function updateThumb() {
    if (!scrollContent || !scrollThumb) return;
    
    const scrollPercentage = scrollContent.scrollTop / (scrollContent.scrollHeight - scrollContent.clientHeight);
    const thumbHeight = Math.max(30, (scrollContent.clientHeight / scrollContent.scrollHeight) * 100);
    
    scrollThumb.style.height = `${thumbHeight}%`;
    scrollThumb.style.transform = `translateY(${scrollPercentage * (100 - thumbHeight)}%)`;
  }
  
  function handleScroll() {
    if (!isDragging) {
      updateThumb();
    }
  }
  
  function handleThumbMouseDown(event: MouseEvent) {
    isDragging = true;
    startY = event.clientY;
    scrollTop = scrollContent.scrollTop;
    document.body.style.cursor = 'grabbing';
    document.body.style.userSelect = 'none';
  }
  
  function handleMouseMove(event: MouseEvent) {
    if (!isDragging) return;
    
    const deltaY = event.clientY - startY;
    const scrollRatio = deltaY / (scrollTrack.clientHeight - scrollThumb.clientHeight);
    scrollContent.scrollTop = scrollTop + scrollRatio * (scrollContent.scrollHeight - scrollContent.clientHeight);
  }
  
  function handleMouseUp() {
    isDragging = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
  }
  
  onMount(() => {
    if (scrollContent) {
      updateThumb();
      scrollContent.addEventListener('scroll', handleScroll);
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }
  });
  
  onDestroy(() => {
    if (scrollContent) {
      scrollContent.removeEventListener('scroll', handleScroll);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    }
  });
  
  // Computed classes
  $: scrollAreaClass = cn("relative overflow-hidden", className);
  $: viewportClass = cn("size-full rounded-[inherit] overflow-auto");
  $: scrollbarClass = cn(
    "flex touch-none p-px transition-colors select-none",
    orientation === 'vertical' ? "h-full w-2.5 border-l border-l-transparent" : "h-2.5 flex-col border-t border-t-transparent"
  );
  $: thumbClass = cn("bg-border relative flex-1 rounded-full cursor-grab active:cursor-grabbing");
</script>

<div class={scrollAreaClass} {...$$restProps}>
  <div
    bind:this={scrollContent}
    class={viewportClass}
    on:scroll={handleScroll}
  >
    <slot />
  </div>
  
  {#if orientation === 'vertical'}
    <div class="absolute top-0 right-0 h-full w-2.5">
      <div
        bind:this={scrollTrack}
        class={scrollbarClass}
      >
        <div
          bind:this={scrollThumb}
          class={thumbClass}
          role="scrollbar"
          on:mousedown={handleThumbMouseDown}
        ></div>
      </div>
    </div>
  {/if}
</div>
