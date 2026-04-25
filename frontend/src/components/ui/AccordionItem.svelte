<script lang="ts">
  import { getContext } from 'svelte';
  import { cn } from "@/lib/utils";
  // IMPORTANTE: Cambia 'lucide-react' por 'lucide-svelte'  
  import { ChevronDown } from "lucide-svelte";
  import { slide } from "svelte/transition";
  import type { Writable } from 'svelte/store';

  export let value: string;
  export let className: string = "";
  export let title: string = "";

  // Definimos la interfaz para que TypeScript no se queje de 'unknown'
  interface AccordionContext {
    activeItems: Writable<Set<string>>;
    toggleItem: (value: string) => void;
  }

  // Le decimos a TS que el contexto tiene la forma de AccordionContext
  const { activeItems, toggleItem } = getContext<AccordionContext>('accordion');
  
  // Usamos el símbolo $ para acceder al valor de la store de forma reactiva
  $: isOpen = $activeItems.has(value);
</script>

<div class={cn("border-b last:border-b-0", className)}>
  <button
    type="button"
    class="flex flex-1 items-center justify-between w-full py-4 text-sm font-medium transition-all hover:underline outline-none"
    on:click={() => toggleItem(value)}
  >
    <span>{title}</span>
    <svelte:component 
      this={ChevronDown} 
      class={cn(
        "size-4 shrink-0 transition-transform duration-200 text-slate-500",
        isOpen && "rotate-180"
      )} 
    />
  </button>

  {#if isOpen}
    <div transition:slide={{ duration: 200 }}>
      <div class="pt-0 pb-4 text-sm text-slate-600">
        <slot />
      </div>
    </div>
  {/if}
</div>