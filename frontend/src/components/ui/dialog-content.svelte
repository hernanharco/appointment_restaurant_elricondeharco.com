<script lang="ts">
  import { cn } from "../../lib/utils";
  import { X } from "lucide-svelte"; // Necesitarás instalar lucide-svelte si no lo tienes

  // En Svelte 5 usamos $props() para recibir los hijos (children) y las clases
  let { class: className = '', children, ...rest } = $props();
</script>

<div class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"></div>

<div class="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-white p-6 shadow-lg duration-200 sm:rounded-lg">
  
  {@render children?.()}

  </div>

<style>
  /* Podrías añadir animaciones de entrada aquí si quieres darle más valor */
</style>