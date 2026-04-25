import { departmentService } from '@/lib/api/department';
import { departmentStore } from '@/lib/state/department-state.svelte';
import { toastStore } from '@/lib/state/toast-state.svelte'; // Tu store ya creado
import { DEPARTMENT_COLORS, DEFAULT_APP_COLOR } from '@/lib/constants/colors'
import { confirmationStore } from '@/components/shared/state/confirmation-state.svelte';

export class DepartmentFormManager {
  showForm = $state(false);
  isSaving = $state(false);
  // 🎨 Añadimos 'color' al formData con un valor por defecto
  formData = $state({ 
    id: null as number | null, 
    name: '', 
    description: '', 
    color: DEFAULT_APP_COLOR, // Azul por defecto
    is_active: true 
  });

  // Lista de colores predefinidos (Tailwind 600)
  // 🎨 Ya no definimos el array aquí, lo traemos de la fuente única de verdad
  get availableColors() {
    return DEPARTMENT_COLORS;
  }

  showColorPicker = $state(false);

  toggleForm() {
    this.showForm = !this.showForm;
    if (!this.showForm) this.resetForm();
  }

  resetForm() {
    this.formData = { id: null, name: '', description: '', color: DEFAULT_APP_COLOR, is_active: true };
    this.showForm = false;
    this.showColorPicker = false;
  }

  selectColor(hex: string) {
    this.formData.color = hex;
    this.showColorPicker = false;
  }

  startEdit(dept: any) {
    this.formData = { ...dept };
    this.showForm = true;
  }

  async save() {
    if (!this.formData.name.trim()) {
      toastStore.show('El nombre es obligatorio', 'info');
      return;
    }

    this.isSaving = true;
    try {
      if (this.formData.id) {
        await departmentService.update(this.formData.id, this.formData);
        toastStore.show('Departamento actualizado correctamente', 'success');
      } else {
        await departmentService.create(this.formData);
        toastStore.show('Nuevo departamento registrado', 'success');
      }

      await departmentStore.refresh();
      this.resetForm();
    } catch (e) {
      toastStore.show('Hubo un error al guardar los cambios', 'error');
      console.error(e);
    } finally {
      this.isSaving = false;
    }
  }

  async delete(id: number | null) {
    if (!id) return;

    // Llamamos a la confirmación "Premium"
    confirmationStore.show({
      title: '¿Eliminar Departamento?',
      message: 'Esta acción es irreversible. Todos los servicios y colaboradores asociados podrían verse afectados.',
      onConfirm: async () => {
        try {
          await departmentService.delete(id);
          toastStore.show('Departamento eliminado del sistema', 'success');
          await departmentStore.refresh();
        } catch (e) {
          toastStore.show('No se pudo eliminar el departamento', 'error');
        }
      }
    });
}
}