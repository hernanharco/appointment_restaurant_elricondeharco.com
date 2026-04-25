<script lang="ts">
  import { 
    Building2, 
    Users, 
    Briefcase, 
    CalendarCheck2, 
    UserCircle,
    RefreshCw // Corregido: Es RefreshCw (minúscula la 'w')
  } from 'lucide-svelte';

  // Importamos las instancias de los stores
  import { departmentStore } from '@/lib/state/department-state.svelte.ts';
  import { collaboratorStore } from '@/lib/state/collaborator-state.svelte.ts';
  import { serviceStore } from '@/lib/state/service-state.svelte.ts';
  import { clientStore } from '@/lib/state/client-state.svelte.ts';
  import { appointmentStore } from '@/lib/stores/appointment-state.svelte';
  
  // Importamos el store de salud
  import { healthStore } from '@/lib/state/health-state.svelte';
  
  const navItems = [
    { id: 'department', name: 'Departamento', icon: Building2, color: 'text-purple-600', bg: 'bg-purple-50' },
    { id: 'collaborators', name: 'Colaboradores', icon: Users, color: 'text-blue-600', bg: 'bg-blue-50' },
    { id: 'services', name: 'Servicios', icon: Briefcase, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { id: 'appointments', name: 'Citas', icon: CalendarCheck2, color: 'text-amber-600', bg: 'bg-amber-50' },
    { id: 'clients', name: 'Clientes', icon: UserCircle, color: 'text-rose-600', bg: 'bg-rose-50' },
  ];

  async function handleOpenModal(id: string) {
    // Bloqueo de seguridad: No abrir modales si estamos offline
    if (!healthStore.isOnline) {
      console.warn("[Navigation] Acción bloqueada: El sistema está offline.");
      return; 
    }

    console.log(`[Navigation] Abriendo: ${id}`);
    
    switch (id) {
      case 'department':
        departmentStore.openDepartmentModal();
        await departmentStore.refresh();
        break;
      case 'collaborators':
        collaboratorStore.open();
        await collaboratorStore.refresh();
        break;
      case 'services':
        serviceStore.open();
        await serviceStore.refresh();
        break;
      case 'clients':
        clientStore.openModal();
        await clientStore.refresh();
        break;
      case 'appointments':
        appointmentStore.openModal();
        await appointmentStore.refreshAll();
        break;
    }
  }
</script>

<nav class="flex flex-wrap items-center gap-2 lg:justify-end">
  {#each navItems as item}
    <button 
      onclick={() => handleOpenModal(item.id)}
      disabled={!healthStore.isOnline}
      class="flex items-center gap-2.5 px-3.5 py-2 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/50 hover:shadow-sm transition-all active:scale-95 group disabled:opacity-50 disabled:cursor-not-allowed disabled:filter disabled:grayscale"
      title={healthStore.isOnline ? `Abrir ${item.name}` : 'Conexión perdida'}
    >
      <div class="p-1.5 rounded-lg {item.bg} {item.color} group-hover:scale-110 transition-transform">
        <svelte:component this={item.icon} size={18} />
      </div>

      <span class="text-sm font-bold text-slate-600 group-hover:text-blue-700 transition-colors">
        {item.name}
      </span>
    </button>
  {/each}
  
  <div class="h-8 w-px bg-slate-100 mx-2 hidden xl:block"></div>
  
  <button 
    onclick={() => healthStore.checkHealth()}
    disabled={healthStore.isChecking}
    class="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all active:scale-95 disabled:opacity-80
    {healthStore.isOnline ? 'bg-emerald-50 border-emerald-100' : 'bg-rose-50 border-rose-100'}"
    title="Click para verificar conexión"
  >
    <div class="relative flex h-2 w-2">
      {#if healthStore.isOnline && !healthStore.isChecking}
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
      {/if}
      <span class="relative inline-flex rounded-full h-2 w-2 {healthStore.isOnline ? 'bg-emerald-500' : 'bg-rose-500'}"></span>
    </div>
    
    <span class="text-[10px] font-bold uppercase tracking-tighter {healthStore.isOnline ? 'text-emerald-600' : 'text-rose-600'}">
      {healthStore.isChecking ? 'Verificando...' : (healthStore.isOnline ? 'Live Sync' : 'Offline')}
    </span>

    <div class={healthStore.isChecking ? 'animate-spin' : ''}>
      <RefreshCw size={10} class={healthStore.isOnline ? 'text-emerald-400' : 'text-rose-400'} />
    </div>
  </button>
</nav>