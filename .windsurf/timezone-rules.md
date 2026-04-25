# 🌍 Regla de Negocio: Gestión de Zona Horaria

## Principio Fundamental para Windsurf

**"En este proyecto, la lógica de tiempo está centralizada en el backend. El backend recibe UTC/Local, valida contra la zona horaria del .env y siempre responde con strings ISO localizados. El frontend debe ser 'pasivo' respecto a la conversión de zonas horarias."**

## 🚫 Qué NO hacer nunca en el frontend:

1. **No calcular offsets manualmente**
   ```typescript
   // ❌ NUNCA hacer esto
   const offset = getTimezoneOffset();
   const localTime = new Date(utcTime + offset * 60000);
   ```

2. **No sumar/restar horas para zona horaria**
   ```typescript
   // ❌ NUNCA hacer esto
   const spanishTime = new Date(utcTime.setHours(utcTime.getHours() + 1));
   ```

3. **No usar librerías de conversión de zona horaria**
   ```typescript
   // ❌ NUNCA hacer esto
   import { zonedTimeToUtc, utcToZonedTime } from 'date-fns-tz';
   ```

4. **No formatear con timezone manual**
   ```typescript
   // ❌ NUNCA hacer esto
   format(date, "yyyy-MM-dd'T'HH:mm:ssXXX", { timeZone: 'Europe/Madrid' });
   ```

## ✅ Qué SÍ hacer siempre:

1. **Enviar UTC simple al backend**
   ```typescript
   // ✅ SIEMPRE así
   start_time: start.toISOString(),
   end_time: end.toISOString(),
   ```

2. **Recibir ISO con offset del backend**
   ```typescript
   // ✅ SIEMPRE así
   start_time: new Date(apt.start_time), // Backend envía: "2026-02-05T11:00:00+01:00"
   ```

3. **Solo formatear para visualización**
   ```typescript
   // ✅ SIEMPRE así (solo para mostrar)
   {format(appointment.start_time, 'HH:mm')}
   ```

## 🎯 Mnemotécnia para Windsurf:

> **"UTC va, ISO viene, frontend muestra"**

## 📋 Checklist al revisar código:

- [ ] ¿Se está enviando `toISOString()` al crear citas?
- [ ] ¿Se está usando `new Date()` para recibir del backend?
- [ ] ¿Solo se usa `format()` para visualización?
- [ ] ¿No hay cálculos manuales de zona horaria?
- [ ] ¿No hay librerías de timezone en el frontend?

## 🔍 Ejemplos Correctos:

### Crear Cita
```typescript
// ✅ Frontend crea UTC simple
const start = new Date(selectedDate);
start.setUTCHours(10, 0, 0, 0);
await appointmentsApi.createAppointment({
  start_time: start.toISOString(), // "2026-02-05T10:00:00.000Z"
  end_time: end.toISOString(),     // "2026-02-05T10:30:00.000Z"
});
```

### Mostrar Cita
```typescript
// ✅ Backend envía ISO con offset, frontend solo muestra
{format(appointment.start_time, 'HH:mm')} // "11:00"
```

---

**RECORDATORIO: El backend es la única fuente de verdad para la zona horaria. El frontend es pasivo.**
