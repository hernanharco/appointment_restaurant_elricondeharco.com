<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let htmlFor: string | undefined = undefined;
  export let className: string = '';
  export let onclick: ((event: MouseEvent) => void) | undefined = undefined;
  export let onkeydown: ((event: KeyboardEvent) => void) | undefined = undefined;
  
  // Handle keyboard events for accessibility
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (onclick) onclick(event as any);
    }
    if (onkeydown) onkeydown(event);
  }
  
  // Computed classes
  $: labelClass = cn(
    "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
    className
  );
</script>

<label
  for={htmlFor}
  class={labelClass}
  class:cursor-pointer={onclick}
  onclick={onclick}
  onkeydown={onclick ? handleKeydown : onkeydown}
  {...$$restProps}
>
  <slot />
</label>
