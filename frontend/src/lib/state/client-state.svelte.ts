import { clientsApi } from '@/lib/api/clients'; 
import type { Client } from '@/types/clients';

class ClientStore {
  #items = $state<Client[]>([]);
  #loading = $state(false);
  #isModalOpen = $state(false);

  get items() { return this.#items; }
  get isLoading() { return this.#loading; }
  get isModalOpen() { return this.#isModalOpen; }

  /**
   * Carga los clientes desde el Backend
   */
  async fetchClients() {
    this.#loading = true;
    try {
      this.#items = await clientsApi.getAll();
    } catch (error) {
      console.error("Error al cargar clientes:", error);
    } finally {
      this.#loading = false;
    }
  }

  async refresh() {
    await this.fetchClients();
  }

  /**
   * 🔍 BÚSQUEDA POR TELÉFONO
   * Responsabilidad: Hablar con la API y devolver el resultado.
   * No debe tocar el formulario directamente, solo devolver los datos.
   */
  async findByPhone(phone: string): Promise<Client | null> {
    const cleanPhone = phone.trim();
    if (cleanPhone.length < 9) return null;

    try {
      // Llamamos a tu método searchByPhone de la API
      return await clientsApi.searchByPhone(cleanPhone);
    } catch (error) {
      console.error("❌ Error en ClientStore.findByPhone:", error);
      return null;
    }
  }

  /**
   * Guarda o Actualiza un cliente.
   */
  async saveClient(formData: any): Promise<Client | null> {
    try {
      let savedClient: Client;
      if (formData.id) {
        savedClient = await clientsApi.update(formData.id, formData);
        this.#items = this.#items.map(c => c.id === savedClient.id ? savedClient : c);
      } else {
        savedClient = await clientsApi.create(formData);
        this.#items = [savedClient, ...this.#items];
      }
      return savedClient;
    } catch (error) {
      console.error("Error en saveClient:", error);
      throw error;
    }
  }

  // Métodos de UI
  openModal() { this.#isModalOpen = true; }
  closeModal() { this.#isModalOpen = false; }
}

export const clientStore = new ClientStore();