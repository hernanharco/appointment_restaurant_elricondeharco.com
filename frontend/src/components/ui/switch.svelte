<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher } from "svelte";
  
  // Props
  export let checked = false;
  export let disabled = false;
  export let required = false;
  export let value = '';
  export let className = '';
  
  const dispatch = createEventDispatcher();
  
  let inputElement: HTMLInputElement;
  
  function handleChange() {
    checked = inputElement.checked;
    dispatch('change', { checked, value });
  }
  
  // Computed classes
  $: switchClass = cn(
    "peer inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full border border-transparent transition-all outline-none focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-50",
    checked 
      ? "bg-primary" 
      : "bg-switch-background dark:bg-input/80",
    className
  );
  
  $: thumbClass = cn(
    "pointer-events-none block size-4 rounded-full ring-0 transition-transform",
    checked 
      ? "translate-x-[calc(100%-2px)] bg-primary-foreground dark:bg-card" 
      : "translate-x-0 bg-card dark:bg-card-foreground"
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
    class={switchClass}
    role="switch"
    aria-checked={checked}
    tabindex={disabled ? -1 : 0}
    on:click={() => inputElement.click()}
    on:keydown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        inputElement.click();
      }
    }}
  >
    <div class={thumbClass}></div>
  </div>
</div>
