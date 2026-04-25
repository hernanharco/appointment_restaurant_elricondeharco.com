<script lang="ts">
  import { toastStore } from '@/lib/state/toast-state.svelte';
  import { fly } from 'svelte/transition';
  import { CheckCircle2, AlertCircle, Info } from 'lucide-svelte';
</script>

<div class="fixed bottom-6 right-6 z-200 flex flex-col gap-2 pointer-events-none">
  {#each toastStore.items as toast (toast.id)}
    <div 
      transition:fly={{ x: 50, duration: 300 }}
      class="pointer-events-auto px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-3 border min-w-[280px]
      {toast.type === 'success' ? 'bg-white border-emerald-100 text-emerald-600' : 
       toast.type === 'error' ? 'bg-rose-50 border-rose-100 text-rose-600' : 
       'bg-indigo-900 border-indigo-800 text-white'}"
    >
      {#if toast.type === 'success'} <CheckCircle2 size={18} />
      {:else if toast.type === 'error'} <AlertCircle size={18} />
      {:else} <Info size={18} />
      {/if}
      
      <span class="text-sm font-bold">{toast.message}</span>
    </div>
  {/each}
</div>