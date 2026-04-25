<script lang="ts">
  import { cn, createVariants } from "../../lib/utils";
  
  // Props
  export let variant: 'default' | 'secondary' | 'destructive' | 'outline' = 'default';
  export let href: string | undefined = undefined;
  export let className = '';
  export let onclick: ((event: MouseEvent) => void) | undefined = undefined;
  
  // Determine if it should render as a link or span
  $: isLink = !!href;
  
  // Badge variants
  const badgeVariants = createVariants(
    "inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-xs font-medium w-fit whitespace-nowrap shrink-0 [&>svg]:size-3 gap-1 [&>svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden",
    {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground [a&]:hover:bg-primary/90",
        secondary: "border-transparent bg-secondary text-secondary-foreground [a&]:hover:bg-secondary/90",
        destructive: "border-transparent bg-destructive text-white [a&]:hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60",
        outline: "text-foreground [a&]:hover:bg-accent [a&]:hover:text-accent-foreground"
      }
    },
    {
      variant: 'default'
    }
  );
  
  // Computed classes
  $: badgeClass = cn(badgeVariants({ variant, class: className }));
</script>

{#if isLink}
  <a
    {href}
    class={badgeClass}
    onclick={onclick}
    role="status"
    {...$$restProps}
  >
    <slot />
  </a>
{:else}
  <span
    class={badgeClass}
    onclick={onclick}
    role="status"
    {...$$restProps}
  >
    <slot />
  </span>
{/if}
