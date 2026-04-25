<script lang="ts">
  import { cn } from "../../lib/utils";
  import { Check } from "lucide-svelte";
  import { createEventDispatcher } from "svelte";
  
  // Props
  export let checked = false;
  export let disabled = false;
  export let required = false;
  export let value = '';
  export let className = '';
  export let indeterminate = false;
  
  const dispatch = createEventDispatcher();
  
  let inputElement: HTMLInputElement;
  
  function handleChange() {
    checked = inputElement.checked;
    dispatch('change', { checked, value });
  }
  
  // Computed classes
  $: checkboxClass = cn(
    "peer border bg-input-background dark:bg-input/30 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground dark:data-[state=checked]:bg-primary data-[state=checked]:border-primary focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive size-4 shrink-0 rounded-[4px] border shadow-xs transition-shadow outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50",
    checked && "bg-primary text-primary-foreground border-primary",
    indeterminate && "bg-primary text-primary-foreground border-primary",
    className
  );
</script>

<div class="relative inline-flex items-center">
  <input
    bind:this={inputElement}
    type="checkbox"
    {checked}
    {disabled}
    {required}
    {value}
    class="sr-only"
    on:change={handleChange}
    on:click
    on:keydown
    {...$$restProps}
  />
  <div
    class={checkboxClass}
    role="checkbox"
    aria-checked={indeterminate ? 'mixed' : checked}
    tabindex={disabled ? -1 : 0}
    on:click={() => inputElement.click()}
    on:keydown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        inputElement.click();
      }
    }}
  >
    {#if checked}
      <Check class="size-3.5" />
    {:else if indeterminate}
      <div class="size-2 bg-current rounded-sm"></div>
    {/if}
  </div>
</div>
