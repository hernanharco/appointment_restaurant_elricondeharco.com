<script lang="ts">
  import { cn } from "../../lib/utils";
  import { ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-svelte";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  // PROPS
  export let currentPage: number = 1;
  export let totalPages: number = 1;
  export let className: string = "";

  // Estilos base de los botones (reutilizando clases de Tailwind para no depender de un componente Button externo si no quieres)
  const buttonBase = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50 h-9 px-3";
  const ghostStyles = "hover:bg-slate-100 hover:text-slate-900";
  const outlineStyles = "border border-slate-200 bg-white shadow-sm hover:bg-slate-100";

  function goToPage(page: number) {
    if (page < 1 || page > totalPages) return;
    dispatch("pageChange", page);
  }
</script>

<nav
  aria-label="pagination"
  class={cn("mx-auto flex w-full justify-center", className)}
>
  <ul class="flex flex-row items-center gap-1">
    <li>
      <button
        on:click={() => goToPage(currentPage - 1)}
        disabled={currentPage === 1}
        class={cn(buttonBase, ghostStyles, "gap-1 pl-2.5")}
        aria-label="Ir a página anterior"
      >
        <ChevronLeft class="size-4" />
        <span class="hidden sm:block">Anterior</span>
      </button>
    </li>

    {#each Array(totalPages) as _, i}
      {@const page = i + 1}
      <li>
        <button
          on:click={() => goToPage(page)}
          class={cn(
            buttonBase,
            "w-9",
            currentPage === page ? outlineStyles : ghostStyles
          )}
          aria-current={currentPage === page ? "page" : undefined}
        >
          {page}
        </button>
      </li>
    {/each}

    <li>
      <button
        on:click={() => goToPage(currentPage + 1)}
        disabled={currentPage === totalPages}
        class={cn(buttonBase, ghostStyles, "gap-1 pr-2.5")}
        aria-label="Ir a página siguiente"
      >
        <span class="hidden sm:block">Siguiente</span>
        <ChevronRight class="size-4" />
      </button>
    </li>
  </ul>
</nav>