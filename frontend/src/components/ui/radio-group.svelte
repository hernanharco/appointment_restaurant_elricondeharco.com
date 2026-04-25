<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher, setContext } from 'svelte';
  import { writable, type Writable } from 'svelte/store';

  // PROPS
  export let value: string = "";
  export let name: string = `radio-group-${Math.random().toString(36).substring(2, 9)}`;
  export let className: string = "";

  const dispatch = createEventDispatcher();
  const selectedValue = writable(value);

  // Sincronizamos la prop 'value' con el store interno
  $: selectedValue.set(value);
  $: value = $selectedValue;

  // Compartimos el estado con los RadioGroupItem hijos
  setContext('radio-group', { selectedValue, name });

  $: dispatch('change', value);
</script>

<div 
  role="radiogroup"
  data-slot="radio-group" 
  class={cn("grid gap-3", className)}
  {...$$restProps}
>
  <slot />
</div>
