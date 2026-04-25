<script lang="ts">
  import { confirmationStore } from '@/components/shared/state/confirmation-state.svelte';
  import { AlertTriangle, Loader2 } from 'lucide-svelte';
  import { fade, scale } from 'svelte/transition';
</script>

{#if confirmationStore.isOpen}
  <div 
    transition:fade={{ duration: 200 }} 
    class="fixed inset-0 z-200 flex items-center justify-center p-4 backdrop-blur-md bg-slate-950/40"
  >
    <div 
      transition:scale={{ start: 0.95, duration: 200 }}
      class="bg-white w-full max-w-sm rounded-[2.5rem] shadow-2xl overflow-hidden border border-slate-100"
    >
      <div class="p-8 text-center">
        <div class="mx-auto w-20 h-20 bg-rose-50 rounded-3xl flex items-center justify-center text-rose-500 mb-6 shadow-inner relative">
            <div class="absolute inset-0 bg-rose-200 blur-2xl opacity-20 animate-pulse"></div>
            <AlertTriangle size={40} strokeWidth={2.5} class="relative" />
        </div>

        <h3 class="text-xl font-black text-slate-900 mb-2 leading-tight">
            {confirmationStore.title}
        </h3>
        <p class="text-sm font-medium text-slate-500 leading-relaxed mb-8 px-2">
          {confirmationStore.message}
        </p>

        <div class="flex flex-col gap-3">
          <button 
            onclick={() => confirmationStore.confirm()}
            disabled={confirmationStore.isLoading}
            class="w-full py-4 bg-rose-500 hover:bg-rose-600 disabled:bg-rose-300 text-white text-[11px] font-black uppercase tracking-[0.15em] rounded-2xl transition-all active:scale-95 shadow-lg shadow-rose-100 flex items-center justify-center gap-3"
          >
            {#if confirmationStore.isLoading}
              <Loader2 size={16} class="animate-spin" />
              Procesando...
            {:else}
              Confirmar y Eliminar
            {/if}
          </button>
          
          <button 
            onclick={() => confirmationStore.close()}
            disabled={confirmationStore.isLoading}
            class="w-full py-4 bg-slate-50 hover:bg-slate-100 disabled:opacity-50 text-slate-500 text-[11px] font-black uppercase tracking-[0.15em] rounded-2xl transition-all active:scale-95"
          >
            No, mantener cambios
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}