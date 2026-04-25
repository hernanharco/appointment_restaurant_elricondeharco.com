// src/lib/stores/auth.ts
import { writable, derived } from 'svelte/store';

export interface User {
  id: number;
  email: string;
  full_name?: string;
  is_active: boolean;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: typeof localStorage !== 'undefined' ? localStorage.getItem('auth_token') : null,
  isLoading: false,
  error: null,
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,

    setLoading: (isLoading: boolean) =>
      update((s) => ({ ...s, isLoading, error: null })),

    setError: (error: string) =>
      update((s) => ({ ...s, error, isLoading: false })),

    login: (token: string, user: User) => {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem('auth_token', token);
      }
      update((s) => ({ ...s, token, user, isLoading: false, error: null }));
    },

    logout: () => {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('auth_token');
      }
      set({ user: null, token: null, isLoading: false, error: null });
    },

    clearError: () => update((s) => ({ ...s, error: null })),
  };
}

export const authStore = createAuthStore();

// Derivados útiles
export const isAuthenticated = derived(authStore, ($auth) => !!$auth.token && !!$auth.user);
export const currentUser = derived(authStore, ($auth) => $auth.user);
export const authToken = derived(authStore, ($auth) => $auth.token);