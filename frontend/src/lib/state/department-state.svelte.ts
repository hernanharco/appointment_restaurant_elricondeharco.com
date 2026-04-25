import { departmentService } from '@/lib/api/department';

// Definimos la interfaz igual a tu tabla de base de datos
export interface Department {
  id: number | null;
  name: string;
  description: string;
  color: string;
  is_active: boolean; // Agregado según tu DB
}

export const departmentStore = $state({
  isDepartmentModalOpen: false,
  departments: [] as Department[], // Tipamos la lista
  loading: false,

  openDepartmentModal() {
    this.isDepartmentModalOpen = true;
  },

  closeDepartmentModal() {
    this.isDepartmentModalOpen = false;
  },

  async refresh() {
    this.loading = true;
    try {
      this.departments = await departmentService.getAll();
    } catch (error) {
      console.error("Error al cargar:", error);
    } finally {
      this.loading = false;
    }
  }
});