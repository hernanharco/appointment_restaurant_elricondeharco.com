<script lang="ts">
  import { cn } from "../../lib/utils";
  import { Search } from "lucide-svelte";
  import { createEventDispatcher, setContext } from "svelte";
  import { writable } from "svelte/store";

  // PROPS
  export let className: string = "";
  export let placeholder: string = "Escribe un comando o busca...";
  export let value: string = "";

  const dispatch = createEventDispatcher();

  // ESTADO INTERNO
  let items: HTMLElement[] = [];
  let selectedIndex = 0;
  const searchTerm = writable("");

  // Contexto para que los items sepan qué mostrar
  setContext("command", {
    searchTerm,
  });

  $: searchTerm.set(value);

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
      items[selectedIndex]?.focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
      items[selectedIndex]?.focus();
    } else if (e.key === "Enter") {
      items[selectedIndex]?.click();
    }
  }

  function onInput(e: Event) {
    value = (e.target as HTMLInputElement).value;
    dispatch("input", value);
  }
</script>

<button
  type="button"
  on:keydown={handleKeyDown}
  class={cn(
    "bg-white text-slate-950 flex h-full w-full flex-col overflow-hidden rounded-md border shadow-md",
    className
  )}
  data-slot="command"
>
  <div class="flex items-center border-b px-3" data-slot="command-input-wrapper">
    <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
    <input
      bind:value
      on:input={onInput}
      {placeholder}
      class="flex h-11 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
    />
  </div>

  <div class="max-h-[300px] overflow-y-auto overflow-x-hidden p-1">
    <slot />
  </div>
</button>