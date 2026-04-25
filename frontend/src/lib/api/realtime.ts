// src/lib/api/realtime.ts
import { API_ROUTES } from '../../config/api'; // Asegúrate de que la ruta sea correcta
import type { MariaNotification } from '@/types/notifications';

const BASE_URL = import.meta.env.PUBLIC_API_BACKEND;

export const realtimeService = {
  /**
   * 📡 Conecta al stream SSE usando la configuración centralizada.
   */
  connect(onUpdate: (data: MariaNotification) => void) {
    // 1. Evitamos conexiones duplicadas (limpieza preventiva)
    if ((window as any).sseConnection) {
      (window as any).sseConnection.close();
      console.log("🔄 Reiniciando conexión SSE previa...");
    }

    // 2. Construimos la URL dinámicamente
    const url = `${BASE_URL}${API_ROUTES.NOTIFICATIONS.STREAM}`;

    // 3. Abrimos la conexión con soporte para Cookies (httpOnly)
    const eventSource = new EventSource(url, { withCredentials: true });

    console.log(`🔗 Intentando conectar al stream en: ${url}`);

    eventSource.addEventListener('update', (event) => {
      try {
        const rawData = event.data;

        // 🧠 LÓGICA DE COMPATIBILIDAD:
        // Si es el string "refresh", creamos el objeto. Si es JSON, lo parseamos.
        const parsedData: MariaNotification = rawData === 'refresh'
          ? { type: 'REFRESH' }
          : JSON.parse(rawData);

        console.log("📥 Notificación recibida:", parsedData);
        onUpdate(parsedData);
      } catch (err) {
        console.error('❌ Error parseando mensaje de María:', err);
      }
    });

    eventSource.onerror = (err) => {
      // Importante: No cerramos aquí para que EventSource intente reconectar solo
      console.warn('⚠️ SSE Error o conexión perdida. EventSource reintentará automáticamente.', err);
    };

    // Guardamos la referencia global
    (window as any).sseConnection = eventSource;

    // Retornamos una función de limpieza (útil para useEffect/onDestroy)
    return () => {
      eventSource.close();
      (window as any).sseConnection = null;
    };
  }
};