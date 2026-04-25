// lib/state/toast-state.svelte.ts
export type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

export const toastStore = $state({
  items: [] as Toast[],

  show(message: string, type: ToastType = 'success') {
    const id = Date.now();
    this.items.push({ id, message, type });

    // Auto-eliminar después de 3 segundos
    setTimeout(() => {
      this.items = this.items.filter(t => t.id !== id);
    }, 3000);
  }
});