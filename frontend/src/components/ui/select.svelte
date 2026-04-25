<script lang="ts">
  import { cn } from "../../lib/utils";
  import { ChevronDown, Check, ChevronUp, ChevronLeft, ChevronRight } from "lucide-svelte";
  import { createEventDispatcher, onMount } from "svelte";
  
  // Props
  export let value = '';
  export let placeholder = '';
  export let disabled = false;
  export let className = '';
  export let size: 'sm' | 'default' = 'default';
  export let items: Array<{ value: string; label: string; disabled?: boolean }> = [];
  
  const dispatch = createEventDispatcher();
  
  let isOpen = false;
  let triggerElement: HTMLButtonElement;
  let contentElement: HTMLDivElement;
  let highlightedIndex = 0;
  
  $: selectedLabel = items.find(item => item.value === value)?.label || placeholder;
  $: filteredItems = items;
  
  function toggle() {
    if (disabled) return;
    isOpen = !isOpen;
    if (isOpen) {
      highlightedIndex = items.findIndex(item => item.value === value) || 0;
    }
  }
  
  function selectItem(itemValue: string) {
    value = itemValue;
    isOpen = false;
    dispatch('change', { value: itemValue });
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (disabled) return;
    
    switch (event.key) {
      case 'Enter':
      case ' ':
        event.preventDefault();
        if (isOpen) {
          selectItem(filteredItems[highlightedIndex]?.value);
        } else {
          toggle();
        }
        break;
      case 'ArrowDown':
        event.preventDefault();
        if (!isOpen) {
          toggle();
        } else {
          highlightedIndex = Math.min(highlightedIndex + 1, filteredItems.length - 1);
        }
        break;
      case 'ArrowUp':
        event.preventDefault();
        if (!isOpen) {
          toggle();
        } else {
          highlightedIndex = Math.max(highlightedIndex - 1, 0);
        }
        break;
      case 'Escape':
        event.preventDefault();
        isOpen = false;
        break;
    }
  }
  
  function handleClickOutside(event: MouseEvent) {
    if (!triggerElement?.contains(event.target as Node) && 
        !contentElement?.contains(event.target as Node)) {
      isOpen = false;
    }
  }
  
  onMount(() => {
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  });
  
  $: triggerClass = cn(
    "border-input data-placeholder:text-muted-foreground [&_svg:not([class*='text-'])]:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 dark:hover:bg-input/50 flex w-full items-center justify-between gap-2 rounded-md border bg-input-background px-3 py-2 text-sm whitespace-nowrap transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50",
    size === 'default' ? 'h-9' : 'h-8',
    className
  );
  
  $: contentClass = cn(
    "bg-popover text-popover-foreground data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 relative z-50 max-h-60 min-w-32 origin-[var(--radix-select-content-transform-origin)] overflow-x-hidden overflow-y-auto rounded-md border shadow-md",
    "translate-y-1"
  );
</script>

<div class="relative">
  <button
    bind:this={triggerElement}
    type="button"
    class={triggerClass}
    {disabled}
    on:click={toggle}
    on:keydown={handleKeydown}
    aria-expanded={isOpen}
    aria-haspopup="listbox"
    aria-controls="select-listbox"
    role="combobox"
  >
    <span class="truncate">{selectedLabel}</span>
    <ChevronDown class="size-4 opacity-50 shrink-0" />
  </button>
  
  {#if isOpen}
    <div
      bind:this={contentElement}
      class={contentClass}
      style="position: absolute; top: 100%; left: 0; right: 0; z-index: 50;"
      id="select-listbox"
      role="listbox"
      tabindex="-1"
      aria-activedescendant={`option-${highlightedIndex}`}
    >
      <div class="p-1">
        {#each filteredItems as item, i}
          <div
            id="option-{i}"
            class={cn(
              "focus:bg-accent focus:text-accent-foreground [&_svg:not([class*='text-'])]:text-muted-foreground relative flex w-full cursor-default items-center gap-2 rounded-sm py-1.5 pr-8 pl-2 text-sm outline-hidden select-none data-disabled:pointer-events-none data-disabled:opacity-50",
              item.value === value && "bg-accent text-accent-foreground",
              i === highlightedIndex && "bg-accent text-accent-foreground",
              item.disabled && "opacity-50 cursor-not-allowed"
            )}
            role="option"
            tabindex={i === highlightedIndex ? 0 : -1}
            aria-selected={item.value === value}
            aria-disabled={item.disabled}
            on:click={() => !item.disabled && selectItem(item.value)}
            on:mouseenter={() => highlightedIndex = i}
            on:keydown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (!item.disabled) selectItem(item.value);
              }
            }}
          >
            <span class="absolute right-2 flex size-3.5 items-center justify-center">
              {#if item.value === value}
                <Check class="size-4" />
              {/if}
            </span>
            <span class="truncate">{item.label}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
