<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher } from 'svelte';
  
  // Props
  export let value = 0;
  export let min = 0;
  export let max = 100;
  export let step = 1;
  export let disabled = false;
  export let className = '';
  export let orientation: 'horizontal' | 'vertical' = 'horizontal';
  
  const dispatch = createEventDispatcher();
  
  let isDragging = false;
  let sliderElement: HTMLDivElement;
  let trackElement: HTMLDivElement;
  let thumbElement: HTMLDivElement;
  
  function updateValue(clientX: number, clientY: number) {
    if (!trackElement) return;
    
    const rect = trackElement.getBoundingClientRect();
    let percentage: number;
    
    if (orientation === 'horizontal') {
      percentage = (clientX - rect.left) / rect.width;
    } else {
      percentage = (clientY - rect.top) / rect.height;
    }
    
    percentage = Math.max(0, Math.min(1, percentage));
    const newValue = min + percentage * (max - min);
    const steppedValue = Math.round(newValue / step) * step;
    
    value = Math.max(min, Math.min(max, steppedValue));
    dispatch('change', { value });
  }
  
  function handleMouseDown(event: MouseEvent) {
    if (disabled) return;
    
    isDragging = true;
    updateValue(event.clientX, event.clientY);
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  }
  
  function handleMouseMove(event: MouseEvent) {
    if (!isDragging) return;
    updateValue(event.clientX, event.clientY);
  }
  
  function handleMouseUp() {
    isDragging = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (disabled) return;
    
    let newValue = value;
    
    switch (event.key) {
      case 'ArrowLeft':
      case 'ArrowDown':
        event.preventDefault();
        newValue = Math.max(min, value - step);
        break;
      case 'ArrowRight':
      case 'ArrowUp':
        event.preventDefault();
        newValue = Math.min(max, value + step);
        break;
      case 'Home':
        event.preventDefault();
        newValue = min;
        break;
      case 'End':
        event.preventDefault();
        newValue = max;
        break;
    }
    
    if (newValue !== value) {
      value = newValue;
      dispatch('change', { value });
    }
  }
  
  // Computed classes
  $: sliderClass = cn(
    "relative flex items-center",
    orientation === 'horizontal' ? "w-full" : "h-full flex-col",
    disabled && "opacity-50 cursor-not-allowed",
    className
  );
  
  $: trackClass = cn(
    "relative bg-secondary rounded-full",
    orientation === 'horizontal' ? "h-2 w-full" : "h-full w-2"
  );
  
  $: fillClass = cn(
    "absolute bg-primary rounded-full",
    orientation === 'horizontal' ? "h-full" : "w-full"
  );
  
  $: thumbClass = cn(
    "absolute bg-primary border-2 border-primary-foreground rounded-full shadow-md focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
    disabled && "cursor-not-allowed"
  );
  
  // Calculate positions
  $: percentage = ((value - min) / (max - min)) * 100;
  $: fillStyle = orientation === 'horizontal' 
    ? `width: ${percentage}%` 
    : `height: ${percentage}%`;
  $: thumbStyle = orientation === 'horizontal'
    ? `left: ${percentage}%`
    : `top: ${percentage}%`;
</script>

<div
  class={sliderClass}
  role="slider"
  aria-valuemin={min}
  aria-valuemax={max}
  aria-valuenow={value}
  aria-disabled={disabled}
  tabindex={disabled ? -1 : 0}
  on:keydown={handleKeydown}
  {...$$restProps}
>
  <div
    bind:this={trackElement}
    class={trackClass}
    role="slider"
    on:mousedown={handleMouseDown}
  >
    <div class={fillClass} style={fillStyle}></div>
    <div
      bind:this={thumbElement}
      class={thumbClass}
      style={thumbStyle}
      tabindex={disabled ? -1 : 0}
      role="button"
      aria-label="Slider thumb"
    ></div>
  </div>
</div>
