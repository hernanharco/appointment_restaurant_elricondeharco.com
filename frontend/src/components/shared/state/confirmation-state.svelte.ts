// src/lib/shared/confirmation-state.svelte.ts
class ConfirmationStore {
    isOpen = $state(false);
    isLoading = $state(false); // 🚀 Para controlar el spinner del botón
    title = $state('');
    message = $state('');
    onConfirm: (() => Promise<void> | void) | null = null;
    isDestructive = $state(true);

    show(config: { title: string; message: string; onConfirm: () => Promise<void> | void; isDestructive?: boolean }) {
        this.title = config.title;
        this.message = config.message;
        this.onConfirm = config.onConfirm;
        this.isDestructive = config.isDestructive ?? true;
        this.isOpen = true;
        this.isLoading = false; 
    }

    close() {
        if (this.isLoading) return; // 🛡️ Evitamos cerrar si se está ejecutando la acción
        this.isOpen = false;
        this.onConfirm = null;
    }

    async confirm() {
        if (!this.onConfirm || this.isLoading) return;
        
        try {
            this.isLoading = true;
            await this.onConfirm(); // ⏳ Esperamos a que la API responda
            this.isOpen = false;
        } catch (error) {
            console.error("Error en confirmación:", error);
        } finally {
            this.isLoading = false;
        }
    }
}

export const confirmationStore = new ConfirmationStore();