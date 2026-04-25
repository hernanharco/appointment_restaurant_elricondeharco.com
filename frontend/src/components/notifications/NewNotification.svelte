<script lang="ts">
  import { Sparkles, RefreshCw, X } from 'lucide-svelte';
  import { fly } from 'svelte/transition';
  import { appointmentStore } from '@/lib/stores/appointment-state.svelte.ts';
  import type { MariaNotification as MariaType } from '@/types/notifications';

  // Derivamos la notificación directamente del store
  const notification = $derived(appointmentStore.currentNotification as MariaType | null);

  async function handleNotificationRefresh() {
    await appointmentStore.refreshAll();
    appointmentStore.clearNotification();
  }
</script>

{#if notification}
  <div 
    transition:fly={{ x: 40, duration: 400 }} 
    class="fixed top-12 right-12 z-9999 w-85 pointer-events-auto"
  >
    <div class="bg-slate-900/95 backdrop-blur-2xl border-l-4 border-[#ff007a] rounded-4xl shadow-[0_25px_60px_rgba(0,0,0,0.5)] p-5 text-white border ring-1 ring-black/50">
      <div class="flex items-start gap-4">
        <div class="bg-[#ff007a] p-2 rounded-xl shadow-[0_0_20px_rgba(255,0,122,0.6)] animate-pulse">
          <Sparkles class="w-5 h-5 text-white" />
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="font-black text-[10px] uppercase tracking-[0.2em] text-[#ff007a] mb-1">María a programado una cita nueva:</h3>
          <p class="text-sm font-black text-white truncate uppercase tracking-tight">{notification.client}</p>
          <p class="text-[11px] text-slate-400 font-medium truncate mt-0.5">
            {notification.service} — <span class="text-fuchsia-400 font-bold">{notification.time}</span>
          </p>
        </div>
        <button 
          onclick={() => appointmentStore.clearNotification()} 
          class="p-1 hover:bg-white/10 rounded-lg transition-colors text-slate-500 hover:text-white"
        >
          <X size={20} />
        </button>
      </div>
      
      <button 
        onclick={handleNotificationRefresh} 
        class="mt-5 w-full bg-[#ff007a] hover:bg-[#e6006e] text-white text-[11px] font-black uppercase py-4 rounded-2xl transition-all shadow-[0_10px_20px_rgba(255,0,122,0.3)] flex items-center justify-center gap-3 group active:scale-95"
      >
        <RefreshCw size={14} class="group-hover:rotate-180 transition-transform duration-700" />
        Actualizar Agenda
      </button>
    </div>
  </div>
{/if}