<script lang="ts">
  import { cn } from "@/lib/utils";
  import { ChevronDown } from "lucide-svelte";
  import { slide } from "svelte/transition";

  // Props del contenedor principal
  export let className: string = "";
  export let type: "single" | "multiple" = "single";

  // Estado para controlar qué items están abiertos
  let openItems = new Set();

  function toggleItem(value: string) {
    if (type === "single") {
      openItems = openItems.has(value) ? new Set() : new Set([value]);
    } else {
      if (openItems.has(value)) {
        openItems.delete(value);
      } else {
        openItems.add(value);
      }
      openItems = openItems; // Forzar reactividad
    }
  }

  // Proveemos el estado a los componentes hijos mediante contexto de Svelte
  import { setContext } from 'svelte';
  import { writable } from 'svelte/store';
  
  const activeItems = writable(openItems);
  $: activeItems.set(openItems);

  setContext('accordion', {
    activeItems,
    toggleItem
  });
</script>

<div class={cn("w-full", className)}>
  <slot />
</div>