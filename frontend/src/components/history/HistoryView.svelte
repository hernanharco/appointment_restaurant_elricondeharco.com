<script lang="ts">
  import { onMount } from 'svelte';
  import apiCentralized from '@/services/api-centralized.ts';

  let reservations = $state<any[]>([]);
  let stats = $state<any>(null);
  let loading = $state(false);
  let error = $state('');

  // Filtros
  let startDate = $state('');
  let endDate = $state('');
  let statusFilter = $state('');
  let searchQuery = $state('');
  let page = $state(1);
  let totalPages = $state(1);
  let total = $state(0);

  const STATUSES = [
    { value: '', label: 'Todos' },
    { value: 'scheduled', label: 'Programadas' },
    { value: 'confirmed', label: 'Confirmadas' },
    { value: 'in_progress', label: 'En curso' },
    { value: 'completed', label: 'Completadas' },
    { value: 'cancelled', label: 'Canceladas' },
    { value: 'no_show', label: 'No asistió' },
  ];

  async function loadData() {
    loading = true;
    error = '';
    try {
      const [historyRes, statsRes] = await Promise.all([
        apiCentralized.getHistory({
          page, per_page: 50,
          start_date: startDate || undefined,
          end_date: endDate || undefined,
          status: statusFilter || undefined,
          search: searchQuery || undefined,
        }),
        apiCentralized.getStats({
          start_date: startDate || undefined,
          end_date: endDate || undefined,
        }),
      ]);
      reservations = historyRes.items;
      total = historyRes.total;
      totalPages = historyRes.total_pages;
      stats = statsRes;
    } catch (err) {
      error = (err as Error).message || 'Error al cargar historial';
    } finally {
      loading = false;
    }
  }

  function search() {
    page = 1;
    loadData();
  }

  function prevPage() { if (page > 1) { page--; loadData(); } }
  function nextPage() { if (page < totalPages) { page++; loadData(); } }

  function downloadCsv() {
    const url = apiCentralized.getExportCsvUrl({
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      status: statusFilter || undefined,
    });
    window.open(url, '_blank');
  }

  function downloadExcel() {
    const url = apiCentralized.getExportExcelUrl({
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      status: statusFilter || undefined,
    });
    window.open(url, '_blank');
  }

  function getStatusBadge(status: string): string {
    const map: Record<string, string> = {
      confirmed: 'bg-green-100 text-green-700',
      scheduled: 'bg-blue-100 text-blue-700',
      in_progress: 'bg-orange-100 text-orange-700',
      completed: 'bg-gray-100 text-gray-700',
      cancelled: 'bg-red-100 text-red-700',
      no_show: 'bg-purple-100 text-purple-700',
    };
    return map[status] || 'bg-gray-100 text-gray-700';
  }

  function getStatusLabel(status: string): string {
    const map: Record<string, string> = {
      confirmed: 'Confirmada', scheduled: 'Programada',
      in_progress: 'En curso', completed: 'Completada',
      cancelled: 'Cancelada', no_show: 'No asistió',
    };
    return map[status] || status;
  }

  onMount(() => { loadData(); });
</script>

<div class="min-h-screen bg-slate-50 p-6">
  <div class="max-w-7xl mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">📊 Historial de Reservas</h1>
        <p class="text-sm text-slate-500 mt-1">
          Consultá, filtrá y exportá el historial completo de reservas
        </p>
      </div>
      <a
        href="/"
        class="text-sm text-blue-600 hover:text-blue-800 underline underline-offset-4 transition-colors"
      >
        ← Volver al inicio
      </a>
    </div>

    {#if error}
      <div class="mb-4 p-4 bg-red-100 border border-red-200 text-red-700 rounded-xl">{error}</div>
    {/if}

    <!-- Filtros -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm p-5 mb-4">
      <div class="flex flex-wrap items-end gap-3">
        <div>
          <label class="block text-xs font-medium text-slate-500 mb-1">Desde</label>
          <input type="date" bind:value={startDate}
            class="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-500 mb-1">Hasta</label>
          <input type="date" bind:value={endDate}
            class="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-500 mb-1">Estado</label>
          <select bind:value={statusFilter}
            class="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500">
            {#each STATUSES as s}
              <option value={s.value}>{s.label}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-500 mb-1">Buscar</label>
          <input type="text" bind:value={searchQuery} placeholder="Nombre o teléfono..."
            class="px-3 py-2 border border-slate-300 rounded-lg text-sm w-48 focus:ring-2 focus:ring-blue-500"
            onkeydown={(e) => { if (e.key === 'Enter') search(); }} />
        </div>
        <button onclick={search}
          class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
          Filtrar
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    {#if stats}
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
        <div class="bg-white border border-slate-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-slate-800">{stats.total_reservations}</div>
          <div class="text-xs text-slate-500 mt-0.5">Total Reservas</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-slate-800">{stats.total_people}</div>
          <div class="text-xs text-slate-500 mt-0.5">Cubiertos</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-slate-800">{stats.avg_party_size}</div>
          <div class="text-xs text-slate-500 mt-0.5">Promedio pax</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-green-600">{stats.by_status.completed}</div>
          <div class="text-xs text-slate-500 mt-0.5">Completadas</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-red-600">{stats.by_status.cancelled}</div>
          <div class="text-xs text-slate-500 mt-0.5">Canceladas</div>
        </div>
      </div>
    {/if}

    <!-- Tabla -->
    <div class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200">
              <th class="text-left px-4 py-3 font-semibold text-slate-600">Fecha</th>
              <th class="text-left px-4 py-3 font-semibold text-slate-600">Hora</th>
              <th class="text-left px-4 py-3 font-semibold text-slate-600">Cliente</th>
              <th class="text-left px-4 py-3 font-semibold text-slate-600">Teléfono</th>
              <th class="text-center px-4 py-3 font-semibold text-slate-600">Pax</th>
              <th class="text-center px-4 py-3 font-semibold text-slate-600">Estado</th>
              <th class="text-center px-4 py-3 font-semibold text-slate-600">Origen</th>
              <th class="text-left px-4 py-3 font-semibold text-slate-600">Notas</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            {#if loading}
              <tr><td colspan="8" class="text-center py-8 text-slate-400">Cargando...</td></tr>
            {:else if reservations.length === 0}
              <tr><td colspan="8" class="text-center py-8 text-slate-400">No hay reservas para los filtros seleccionados</td></tr>
            {:else}
              {#each reservations as r (r.id)}
                <tr class="hover:bg-slate-50/50 transition-colors">
                  <td class="px-4 py-3 text-slate-700 whitespace-nowrap">
                    {new Date(r.start_time).toLocaleDateString('es-ES')}
                  </td>
                  <td class="px-4 py-3 text-slate-700 whitespace-nowrap">
                    {new Date(r.start_time).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td class="px-4 py-3 font-medium text-slate-800">{r.client_name}</td>
                  <td class="px-4 py-3 text-slate-600">{r.client_phone || '—'}</td>
                  <td class="px-4 py-3 text-center font-semibold">{r.party_size}</td>
                  <td class="px-4 py-3 text-center">
                    <span class="inline-block px-2 py-0.5 rounded-full text-[11px] font-bold {getStatusBadge(r.status)}">
                      {getStatusLabel(r.status)}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center text-slate-500 text-xs">{r.source || 'manual'}</td>
                  <td class="px-4 py-3 text-slate-400 text-xs max-w-[150px] truncate">{r.client_notes || '—'}</td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      {#if totalPages > 1}
        <div class="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-slate-50/50">
          <span class="text-sm text-slate-500">
            Página {page} de {totalPages} ({total} reservas)
          </span>
          <div class="flex gap-2">
            <button onclick={prevPage} disabled={page <= 1}
              class="px-3 py-1.5 text-sm border border-slate-300 rounded-lg hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
              ← Anterior
            </button>
            <button onclick={nextPage} disabled={page >= totalPages}
              class="px-3 py-1.5 text-sm border border-slate-300 rounded-lg hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
              Siguiente →
            </button>
          </div>
        </div>
      {/if}
    </div>

    <!-- Botones de exportación -->
    <div class="flex gap-3 mt-4">
      <button onclick={downloadCsv}
        class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm font-medium hover:bg-emerald-700 transition-colors">
        <span class="material-symbols-outlined text-sm">download</span>
        Exportar CSV
      </button>
      <button onclick={downloadExcel}
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-medium hover:bg-blue-700 transition-colors">
        <span class="material-symbols-outlined text-sm">table_chart</span>
        Exportar Excel
      </button>
    </div>

  </div>
</div>
