<script lang="ts">
  import { cn, createVariants } from "../../lib/utils";
  
  // Props
  export let variant: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link' = 'default';
  export let size: 'default' | 'sm' | 'lg' | 'icon' = 'default';
  export let disabled = false;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let href: string | undefined = undefined;
  export let className: string = '';
  export let onclick: ((event: MouseEvent) => void) | undefined = undefined;
  export let onkeydown: ((event: KeyboardEvent) => void) | undefined = undefined;
  
  // Determine if it should render as a link or button
  $: isLink = !!href;
  
  // Button variants
  const buttonVariants = createVariants(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
    {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60",
        outline: "border bg-background text-foreground hover:bg-accent hover:text-accent-foreground dark:bg-input/30 dark:border-input dark:hover:bg-input/50",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50",
        link: "text-primary underline-offset-4 hover:underline"
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3",
        sm: "h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 rounded-md px-6 has-[>svg]:px-4",
        icon: "size-9 rounded-md"
      }
    },
    {
      variant: 'default',
      size: 'default'
    }
  );
  
  // Handle keyboard events for accessibility
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (onclick) onclick(event as any);
    }
    if (onkeydown) onkeydown(event);
  }
  
  // Computed classes
  $: buttonClass = cn(buttonVariants({ variant, size, class: className }));
</script>

{#if isLink}
  <a
    {href}
    role="button"
    tabindex={disabled ? -1 : 0}
    class={buttonClass}
    class:disabled
    aria-disabled={disabled}
    onclick={onclick}
    onkeydown={handleKeydown}
    {...$$restProps}
  >
    <slot />
  </a>
{:else}
  <button
    {type}
    {disabled}
    tabindex={disabled ? -1 : 0}
    class={buttonClass}
    onclick={onclick}
    onkeydown={onkeydown || handleKeydown}
    {...$$restProps}
  >
    <slot />
  </button>
{/if}
