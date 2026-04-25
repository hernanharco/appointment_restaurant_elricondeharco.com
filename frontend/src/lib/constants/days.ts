// src/lib/constants/days.ts

export const DAYS_LABELS = [
  { id: 0, name: 'Lunes' },
  { id: 1, name: 'Martes' },
  { id: 2, name: 'Miércoles' },
  { id: 3, name: 'Jueves' },
  { id: 4, name: 'Viernes' },
  { id: 5, name: 'Sábado' },
  { id: 6, name: 'Domingo' },
];

/**
 * Traduce el índice de JavaScript (0=Dom, 1=Lun...) 
 * al índice de nuestra base de datos (0=Lun, 6=Dom)
 */
export function mapJsDayToCustomDay(jsDay: number): number {
  // JS: 0 (Dom), 1 (Lun), 2 (Mar), 3 (Mie), 4 (Jue), 5 (Vie), 6 (Sab)
  // Resultado: 6 (Dom), 0 (Lun), 1 (Mar), 2 (Mie), 3 (Jue), 4 (Vie), 5 (Sab)
  return jsDay === 0 ? 6 : jsDay - 1;
}

/**
 * Por si necesitas lo contrario: de BD a JS
 */
export function mapCustomDayToJsDay(customDay: number): number {
  return customDay === 6 ? 0 : customDay + 1;
}