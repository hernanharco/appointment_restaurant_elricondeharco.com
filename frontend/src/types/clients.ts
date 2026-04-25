/**
 * TIPADO DE CLIENTES - CoreAppointment SaaS
 * Refleja la estructura de la base de datos en Neon + Transformaciones de la API.
 */

export interface Client {
  id: number;
  business_id: number;
  full_name: string;
  phone: string;
  email?: string | null;
  
  // 📝 Columna física en la DB (TEXT) para observaciones humanas.
  notes?: string | null;
  
  // ⭐ CAMPO VIRTUAL (Inyectado por la API desde metadata_json)
  // Es vital para que Svelte pinte los Smart Chips fácilmente.
  preferred_collaborator_ids: number[]; 
  
  // 🤖 Reservado para otros datos técnicos de la IA.
  metadata_json: Record<string, any>;
  
  is_active: boolean; 
  source: 'ia' | 'manual' | 'web';
  
  // Estado de la sesión actual
  current_service_id?: number | null;
  current_collaborator_id?: number | null;
  
  created_at: string;
  updated_at?: string | null;
}

/**
 * DTO (Data Transfer Objects) para peticiones API
 */

// Al crear, permitimos enviar la lista de favoritos directamente
export interface CreateClientInput extends Omit<Client, 'id' | 'created_at' | 'updated_at' | 'metadata_json' | 'preferred_collaborator_ids'> {
    preferred_collaborator_ids?: number[];
}

// Al actualizar, todo es opcional excepto el ID que se pasa por URL
export type UpdateClientInput = Partial<CreateClientInput>;