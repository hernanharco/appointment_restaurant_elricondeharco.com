<script lang="ts">
  import { cn } from "../../lib/utils";
  import { createEventDispatcher } from "svelte";

  // PROPS
  export let value: string = "";
  export let maxLength: number = 6;
  export let className: string = "";
  export let disabled: boolean = false;

  const dispatch = createEventDispatcher();

  // ESTADO INTERNO
  let inputs: HTMLInputElement[] = [];
  $: digits = value.split("").concat(Array(maxLength).fill("")).slice(0, maxLength);

  function handleInput(e: Event, index: number) {
    const input = e.target as HTMLInputElement;
    const val = input.value.slice(-1); // Solo tomamos el último carácter

    if (val && index < maxLength - 1) {
      inputs[index + 1].focus();
    }

    // Actualizamos el valor global
    const newDigits = [...digits];
    newDigits[index] = val;
    value = newDigits.join("");
    dispatch("change", value);
  }

  function handleKeyDown(e: KeyboardEvent, index: number) {
    if (e.key === "Backspace" && !digits[index] && index > 0) {
      inputs[index - 1].focus();
    }
  }

  function handlePaste(e: ClipboardEvent) {
    e.preventDefault();
    const pasteData = e.clipboardData?.getData("text").slice(0, maxLength) || "";
    value = pasteData;
    dispatch("change", value);
    
    // Enfocar el último input lleno o el siguiente vacío
    const nextIndex = Math.min(pasteData.length, maxLength - 1);
    inputs[nextIndex]?.focus();
  }
</script>

<div 
  class={cn("flex items-center gap-2", disabled && "opacity-50 pointer-events-none", className)}
  data-slot="input-otp"
>
  {#each Array(maxLength) as _, i}
    <div class="relative">
      <input
        bind:this={inputs[i]}
        type="text"
        inputmode="numeric"
        pattern="[0-9]*"
        value={digits[i]}
        on:input={(e) => handleInput(e, i)}
        on:keydown={(e) => handleKeyDown(e, i)}
        on:paste={handlePaste}
        class={cn(
          "h-10 w-10 rounded-md border border-slate-200 bg-white text-center text-sm font-medium transition-all",
          "focus:z-10 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 outline-none",
          digits[i] ? "border-slate-400" : ""
        )}
        {disabled}
      />
      
      {#if !digits[i] && !disabled}
        <div class="pointer-events-none absolute inset-0 flex items-center justify-center opacity-0 focus-within:opacity-100">
            <div class="h-4 w-px bg-slate-950 animate-pulse"></div>
        </div>
      {/if}
    </div>

    {#if i === Math.floor(maxLength / 2) - 1 && maxLength > 4}
      <div class="text-slate-300">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>
      </div>
    {/if}
  {/each}
</div>

<style>
  /* Animación simple para el caret sin librerías externas */
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
  .animate-pulse {
    animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
</style>