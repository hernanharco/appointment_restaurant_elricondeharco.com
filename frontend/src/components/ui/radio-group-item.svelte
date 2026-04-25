<script lang="ts">
  import { cn } from "../../lib/utils";
  import { getContext } from "svelte";
  import { Circle } from "lucide-svelte";
  
  // Props
  export let value: string;
  export let disabled = false;
  export let className = '';
  
  // Get radio group context
  const radioGroup = getContext('radio-group') as any;
  
  function handleClick() {
    if (!disabled) {
      radioGroup.selectedValue.set(value);
    }
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (disabled) return;
    
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }
  }
  
  // Computed classes
  $: isSelected = $radioGroup.selectedValue === value;
  $: buttonClass = cn(
    "aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
    isSelected && "bg-primary text-primary-foreground",
    className
  );
</script>

<button
  type="button"
  class={buttonClass}
  role="radio"
  aria-checked={isSelected}
  {disabled}
  onclick={handleClick}
  onkeydown={handleKeydown}
  {...$$restProps}
>
  {#if isSelected}
    <Circle class="h-2.5 w-2.5 fill-current text-current" />
  {/if}
</button>
