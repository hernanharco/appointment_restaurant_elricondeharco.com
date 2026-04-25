// src/types/notifications.ts o en el store
export interface MariaNotification {
    type: 'NEW_APPOINTMENT' | 'REFRESH';
    title?: string;
    client?: string;
    service?: string;
    time?: string;
}