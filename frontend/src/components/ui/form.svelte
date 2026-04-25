<script lang="ts" context="module">
  import { getContext, setContext } from 'svelte';
  import { writable, type Writable } from 'svelte/store';

  // Contexto para compartir el estado del campo con Label, Message, etc.
  export interface FormFieldContext {
    id: string;
    error: Writable<string | undefined>;
  }
</script>

<script lang="ts">
  import { cn } from "../../lib/utils";

  // PROPS
  export let className: string = "";
  
  // Generamos un ID único para este campo de formulario
  const id = `form-item-${Math.random().toString(36).substring(2, 9)}`;
  const errorStore = writable<string | undefined>(undefined);

  // Compartimos el ID y el store de errores con los hijos
  setContext('form-field', { id, error: errorStore });

  // Exponemos el error para que el padre pueda controlarlo
  export let error: string | undefined = undefined;
  $: errorStore.set(error);
</script>

<div data-slot="form-item" class={cn("grid gap-2", className)}>
  <slot />
</div>