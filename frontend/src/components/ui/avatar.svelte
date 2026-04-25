<script lang="ts">
  import { cn } from "../../lib/utils";
  
  // Props
  export let className = '';
  export let size: 'sm' | 'default' | 'lg' = 'default';
  
  // Size classes
  const sizeClasses = {
    sm: 'size-8',
    default: 'size-10',
    lg: 'size-12'
  };
  
  // Computed classes
  $: avatarClass = cn(
    "relative flex shrink-0 overflow-hidden rounded-full",
    sizeClasses[size],
    className
  );
</script>

<div class={avatarClass} {...$$restProps}>
  <slot />
</div>
