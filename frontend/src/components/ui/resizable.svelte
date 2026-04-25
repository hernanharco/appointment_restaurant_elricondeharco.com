<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher } from 'svelte';
  
  // Props
  export let direction: 'horizontal' | 'vertical' | 'both' = 'both';
  export let className = '';
  export let minWidth = 0;
  export let minHeight = 0;
  export let maxWidth = Infinity;
  export let maxHeight = Infinity;
  
  const dispatch = createEventDispatcher();
  
  let isResizing = false;
  let startX = 0;
  let startY = 0;
  let startWidth = 0;
  let startHeight = 0;
  let element: HTMLDivElement;
  
  function handleMouseDown(event: MouseEvent) {
    isResizing = true;
    startX = event.clientX;
    startY = event.clientY;
    startWidth = element.offsetWidth;
    startHeight = element.offsetHeight;
    
    document.body.style.cursor = direction === 'vertical' ? 'ns-resize' : 
                              direction === 'horizontal' ? 'ew-resize' : 'nwse-resize';
    document.body.style.userSelect = 'none';
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  }
  
  function handleMouseMove(event: MouseEvent) {
    if (!isResizing) return;
    
    const deltaX = event.clientX - startX;
    const deltaY = event.clientY - startY;
    
    let newWidth = startWidth;
    let newHeight = startHeight;
    
    if (direction === 'horizontal' || direction === 'both') {
      newWidth = Math.max(minWidth, Math.min(maxWidth, startWidth + deltaX));
    }
    
    if (direction === 'vertical' || direction === 'both') {
      newHeight = Math.max(minHeight, Math.min(maxHeight, startHeight + deltaY));
    }
    
    element.style.width = `${newWidth}px`;
    element.style.height = `${newHeight}px`;
    
    dispatch('resize', { width: newWidth, height: newHeight });
  }
  
  function handleMouseUp() {
    isResizing = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  }
  
  // Computed classes
  $: resizableClass = cn(
    "relative overflow-hidden",
    className
  );
  
  $: handleClass = cn(
    "absolute bg-primary/20 hover:bg-primary/40 transition-colors",
    direction === 'horizontal' && "bottom-0 left-0 right-0 h-2 cursor-ew-resize",
    direction === 'vertical' && "top-0 bottom-0 right-0 w-2 cursor-ns-resize",
    direction === 'both' && "bottom-0 right-0 w-4 h-4 cursor-nwse-resize"
  );
</script>

<div
  bind:this={element}
  class={resizableClass}
  {...$$restProps}
>
  <slot />
  <div
    class={handleClass}
    on:mousedown={handleMouseDown}
  ></div>
</div>
