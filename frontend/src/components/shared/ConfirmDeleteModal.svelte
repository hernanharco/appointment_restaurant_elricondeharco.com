<script lang="ts">
  import { fade, scale } from 'svelte/transition';
  import { AlertTriangle, Trash2, X } from 'lucide-svelte';

  interface Props {
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    onClose: () => void;
    isLoading?: boolean;
  }

  let { isOpen, title, message, onConfirm, onClose, isLoading = false }: Props = $props();
</script>

{#if isOpen}
  <div class="fixed inset-0 z-110 flex items-center justify-center p-4">
    <div 
      transition:fade={{ duration: 200 }}
      class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm"
      role="button" 
      tabindex="0"
      onkeydown={(e) => e.key === 'Escape' && onClose()}
      onclick={onClose}
    ></div>

    <div 
      transition:scale={{ start: 0.9, duration: 200 }}
      class="bg-white w-full max-w-sm rounded-[2.5rem] shadow-2xl overflow-hidden relative z-20 border border-slate-100 p-8 text-center"
    >
      <button 
        onclick={onClose}
        class="absolute top-6 right-6 p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
        aria-label="Cerrar"
      >
        <X size={20} />
      </button>

      <div class="w-16 h-16 bg-rose-50 text-rose-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <AlertTriangle size={32} />
      </div>

      <h3 class="text-xl font-black text-slate-900 mb-2">{title}</h3>
      <p class="text-sm text-slate-500 font-medium leading-relaxed mb-8">
        {message}
      </p>

      <div class="flex flex-col gap-3">
        <button 
          onclick={onConfirm}
          disabled={isLoading}
          class="w-full py-4 bg-rose-500 hover:bg-rose-600 text-white rounded-2xl font-bold uppercase tracking-widest text-xs transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {#if isLoading}
            <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          {:else}
            <Trash2 size={16} />
          {/if}
          Confirmar eliminación
        </button>

        <button 
          onclick={onClose}
          class="w-full py-4 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-2xl font-bold uppercase tracking-widest text-xs transition-all"
        >
          Volver atrás
        </button>
      </div>
    </div>
  </div>
{/if}