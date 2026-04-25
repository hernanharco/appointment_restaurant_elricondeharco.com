from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session

from app.agents.routing.intent import Intent
from app.agents.routing.state import RoutingState
from app.services.capacity_service import CapacityService
from app.services.reservation_service import ReservationService
from app.schemas.reservations import ReservationCreate
from app.db.session import SessionLocal
from app.models.clients import Client


def _extract_party_size(state: RoutingState) -> int:
    """Extrae el tamaño del grupo del estado o del input del usuario."""
    # 1) Si ya está detectado en el estado
    if "detected_party_size" in state:
        return state["detected_party_size"]
    
    # 2) Intentar extraer del mensaje actual
    user_text = state.get("user_input", "").lower()
    import re
    
    patterns = [
        r'(\d+)\s*(?:persona|personas)',
        r'(?:para|somos|vamos)\s+(\d+)',
        r'(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_text)
        if match:
            try:
                size = int(match.group(1))
                if 1 <= size <= 20:
                    return size
            except ValueError:
                continue
    
    # 3) Valor por defecto si no se detecta
    return 2  # Mesa para 2 por defecto


def _parse_date_from_text(text: str) -> date:
    """Parsea fechas comunes del texto."""
    text_lower = text.lower().strip()
    today = date.today()
    
    # Fechas relativas
    if text_lower in ["hoy"]:
        return today
    elif text_lower in ["mañana", "manana"]:
        return today + timedelta(days=1)
    elif text_lower in ["pasado mañana", "pasado manana"]:
        return today + timedelta(days=2)
    
    # Días de la semana
    weekdays = {
        "lunes": 0, "martes": 1, "miercoles": 2, "miércoles": 2,
        "jueves": 3, "viernes": 4, "sabado": 5, "sábado": 5, "domingo": 6
    }
    
    for day_name, day_num in weekdays.items():
        if day_name in text_lower:
            days_ahead = (day_num - today.weekday() + 7) % 7
            if days_ahead == 0:  # Si es hoy, nos referimos a la próxima semana
                days_ahead = 7
            return today + timedelta(days=days_ahead)
    
    # Si no se detecta, devolver hoy por defecto
    return today


def _format_available_slots(slots: list, party_size: int) -> str:
    """Formatea los slots disponibles para WhatsApp."""
    if not slots:
        return "❌ No hay mesas disponibles para ese día y tamaño de grupo. ¿Quieres probar otro día?"
    
    lines = [
        f"✅ **Mesas disponibles para {party_size} personas:**\n"
    ]
    
    for i, slot in enumerate(slots[:10], start=1):  # Limitar a 10 opciones
        start_time = slot["start_time"].strftime("%H:%M")
        end_time = slot["end_time"].strftime("%H:%M")
        available = slot["available_capacity"]
        total = slot["total_capacity"]
        
        lines.append(f"  *{i}.* {start_time} - {end_time} ({available}/{total} disponibles)")
    
    lines.append("\n💡 Responde con el número de la opción que prefieras.")
    return "\n".join(lines)


def restaurant_booking_node(state: RoutingState) -> RoutingState:
    """
    Nodo de booking optimizado para restaurante basado en aforo.
    Maneja la lógica de reservas por capacidad en lugar de servicios/collaboradores.
    """
    client_phone = state.get("client_phone")
    client_name = state.get("client_name", "cliente")
    user_input = state.get("user_input", "")
    
    if not client_phone:
        return {
            "response_text": "Necesito tu número de teléfono para gestionar tu reserva.",
            "intent": Intent.FINISH,
        }

    db: Session = SessionLocal()
    
    try:
        # Extraer información clave
        party_size = _extract_party_size(state)
        selected_date = state.get("selected_date") or _parse_date_from_text(user_input)
        
        # Si el usuario está eligiendo un slot específico
        available_slots = state.get("available_slots", [])
        if available_slots and user_input.strip().isdigit():
            slot_index = int(user_input.strip()) - 1
            if 0 <= slot_index < len(available_slots):
                selected_slot = available_slots[slot_index]
                
                # Crear la reserva
                reservation_service = ReservationService(db)
                
                # Buscar o crear cliente
                client = db.query(Client).filter(Client.phone == client_phone).first()
                if not client:
                    client = Client(
                        full_name=client_name,
                        phone=client_phone,
                        source="ia"
                    )
                    db.add(client)
                    db.commit()
                    db.refresh(client)
                
                # Crear la reserva
                reservation_data = ReservationCreate(
                    client_name=client_name,
                    client_phone=client_phone,
                    party_size=party_size,
                    start_time=selected_slot["start_time"],
                    end_time=selected_slot["end_time"],
                    source="ia"
                )
                
                reservation = reservation_service.create_reservation(reservation_data)
                
                return {
                    "response_text": (
                        f"🎉 **¡Reserva confirmada!**\n\n"
                        f"📅 **Fecha:** {selected_date.strftime('%d/%m/%Y')}\n"
                        f"🕐 **Hora:** {selected_slot['start_time'].strftime('%H:%M')} - {selected_slot['end_time'].strftime('%H:%M')}\n"
                        f"👥 **Personas:** {party_size}\n"
                        f"📞 **Teléfono:** {client_phone}\n\n"
                        f"📍 **Dirección:** [Tu dirección aquí]\n\n"
                        f"⏰ **Por favor llega 10 minutos antes.**\n"
                        f"Si necesitas modificar, avísanos con al menos 2 horas de anticipación."
                    ),
                    "intent": Intent.CONFIRMATION,
                    "reservation_id": reservation.id,
                }
            else:
                return {
                    "response_text": "Opción no válida. Por favor, elige un número de la lista.",
                    "intent": Intent.BOOKING,
                }
        
        # Si no hay slots, calcular disponibilidad
        capacity_service = CapacityService(db)
        
        try:
            availability = capacity_service.get_restaurant_availability(selected_date, party_size)
            slots = availability.available_slots
            
            if not slots:
                # Sugerir días alternativos
                tomorrow = selected_date + timedelta(days=1)
                next_week = selected_date + timedelta(days=7)
                
                return {
                    "response_text": (
                        f"❌ No hay mesas disponibles para {party_size} personas el {selected_date.strftime('%d/%m/%Y')}.\n\n"
                        f"¿Te gustaría probar:\n"
                        f"• Mañana ({tomorrow.strftime('%d/%m/%Y')})\n"
                        f"• La próxima semana ({next_week.strftime('%d/%m/%Y')})\n"
                        f"¿O prefieres otro día específico?"
                    ),
                    "intent": Intent.BOOKING,
                    "selected_date": selected_date,
                    "detected_party_size": party_size,
                }
            else:
                # Mostrar opciones disponibles
                return {
                    "response_text": _format_available_slots(slots, party_size),
                    "intent": Intent.BOOKING,
                    "available_slots": [slot.__dict__ for slot in slots],
                    "selected_date": selected_date,
                    "detected_party_size": party_size,
                }
                
        except ValueError as e:
            return {
                "response_text": f"No puedo procesar esa reserva: {str(e)}",
                "intent": Intent.FINISH,
            }
            
    except Exception as e:
        return {
            "response_text": "Hubo un error al procesar tu reserva. Por favor, intenta de nuevo o contacta directamente.",
            "intent": Intent.FINISH,
        }
    finally:
        db.close()
