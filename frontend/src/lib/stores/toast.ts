import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'info';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

export const toasts = writable<Toast[]>([]);

export const addToast = (message: string, type: ToastType = 'success') => {
  const id = Math.random();
  toasts.update((all) => [{ id, message, type }, ...all]);

  // Se borra automáticamente después de 3 segundos
  setTimeout(() => {
    toasts.update((all) => all.filter((t) => t.id !== id));
  }, 3000);
};