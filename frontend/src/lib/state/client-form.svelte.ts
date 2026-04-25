/**
 * client-form.svelte.ts
 * Responsabilidad: Gestionar el estado del formulario de clientes y su persistencia.
 * Stack: Svelte 5 (Runes).
 * [cite: 2026-02-23]
 */
import { clientStore } from './client-state.svelte';
import { toastStore } from './toast-state.svelte';

export class ClientFormManager {
    // --- Estado Reactivo (Runes) ---
    formData = $state({
        id: null as number | null,
        full_name: '',
        phone: '',
        email: '',
        notes: '',
        source: 'manual' as 'manual' | 'ia',
        // Lista plana de IDs para la UI del formulario
        preferred_collaborator_ids: [] as number[]
    });

    isSaving = $state(false);
    saveSuccess = $state(false);

    /**
     * Limpia el formulario a sus valores iniciales
     */
    resetForm() {
        this.formData.id = null;
        this.formData.full_name = '';
        this.formData.phone = '';
        this.formData.email = '';
        this.formData.notes = '';
        this.formData.source = 'manual';
        this.formData.preferred_collaborator_ids = [];
        this.saveSuccess = false;
    }

    /**
     * Gestiona la selección/deselección de colaboradores favoritos
     */
    toggleCollaborator(id: number) {
        const current = this.formData.preferred_collaborator_ids;
        if (current.includes(id)) {
            this.formData.preferred_collaborator_ids = current.filter(favId => favId !== id);
        } else {
            this.formData.preferred_collaborator_ids = [...current, id];
        }
    }

    /**
     * Limpia espacios del teléfono para consistencia en DB
     */
    handlePhoneInput(value: string) {
        this.formData.phone = value.replace(/\s/g, '');
    }

    /**
     * Persiste los datos en la base de datos (Neon PostgreSQL)
     */
    async save() {
        // Validaciones básicas antes de disparar infraestructura
        if (!this.formData.full_name.trim() || this.formData.phone.trim().length < 9) {
            toastStore.show('Nombre y Teléfono son obligatorios', 'error');
            return;
        }

        this.isSaving = true;

        try {
            /**
             * 🧠 ESTRUCTURA METADATA_JSON
             * Encapsulamos en 'profile' para separar datos de negocio de la memoria de la IA.
             */
            const clientPayload: any = {
                full_name: this.formData.full_name.trim(),
                phone: this.formData.phone.trim(),
                email: this.formData.email?.trim() || null,
                notes: this.formData.notes?.trim() || "",
                metadata_json: {
                    profile: {
                        preferred_collaborator_ids: this.formData.preferred_collaborator_ids,
                        updated_at: new Date().toISOString()
                    }
                    // 'ai_memory' se mantiene intacto en el backend/DB
                }
            };

            /**
             * 🛡️ REGLA DE NEGOCIO: Proteger el Source
             * Solo enviamos el source si es un registro nuevo (id === null).
             * Si estamos editando, el backend no debe recibirlo para no sobrescribir 
             * si fue creado por la IA originalmente.
             */
            if (!this.formData.id) {
                clientPayload.source = this.formData.source;
            }

            const result = await clientStore.saveClient(this.formData.id 
                ? { ...clientPayload, id: this.formData.id } 
                : clientPayload
            );

            if (result) {
                if (!this.formData.id) this.formData.id = result.id;
                this.saveSuccess = true;
                toastStore.show(this.formData.id ? '¡Ficha actualizada!' : '¡Cliente registrado!', 'success');
                
                // Feedback visual de éxito
                setTimeout(() => { this.saveSuccess = false; }, 2000);
            }
        } catch (error: any) {
            console.error("❌ Error en ClientFormManager:", error);
            toastStore.show(error.message || 'Error al procesar la solicitud', 'error');
        } finally {
            this.isSaving = false;
        }
    }

    /**
     * Cierra el flujo del formulario y resetea el estado
     */
    closeAndReset(callback: () => void) {
        this.resetForm();
        callback();
    }
}