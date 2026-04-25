from app.agents.routing.intent import Intent
from app.agents.routing.state import RoutingState


GREETINGS = {"hola", "buenas", "buenos dias", "buenas tardes", "menu", "inicio", "reiniciar"}

FAREWELL_KEYWORDS = {
    "gracias", "muchas gracias", "ok gracias", "listo gracias",
    "hasta luego", "hasta pronto", "nos vemos", "chao", "chau",
    "bye", "adios", "adiós", "hasta mañana", "hasta manana",
    "perfecto gracias", "de acuerdo gracias", "genial gracias",
    "todo bien gracias", "excelente gracias", "listo muchas gracias",
}

MODIFICATION_KEYWORDS = [
    "cancelar", "cancel", "cancelar reserva", "anular",
    "modificar", "cambiar reserva", "cambiar mi reserva",
    "reprogramar", "mover la reserva", "mover mi reserva",
    "eliminar reserva", "borrar reserva", "quiero cancelar",
    "quiero modificar", "quiero cambiar mi reserva",
]

TIME_FILTER_KEYWORDS = [
    "tarde", "noche", "temprano",
    "antes de", "después de", "despues de",
    "entre las", "a las",
    "tienes para", "hay para", "tenés para",
    "por la", "para la", "en la",
    "ultima hora", "última hora",
    "primer hora", "primera hora",
    "a ultima", "a última",
    "a primera",
]

DATE_KEYWORDS = [
    "mañana", "manana", "hoy", "pasado",
    "otro día", "otro dia", "otra fecha",
    "siguiente", "próximo", "proximo",
    "lunes", "martes",
    "miercoles", "miércoles",
    "jueve", "jueves",
    "viernes",
    "sabado", "sábado", "domingo",
]

# --- NUEVOS KEYWORDS PARA RESTAURANTE ---
PARTY_SIZE_KEYWORDS = [
    "persona", "personas", "comensales", "gente", "grupo",
    "para", "somos", "vamos", "caben", "mesa para",
    "1 persona", "2 personas", "3 personas", "4 personas", "5 personas",
    "6 personas", "7 personas", "8 personas", "9 personas", "10 personas",
    "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"
]

CAPACITY_KEYWORDS = [
    "capacidad", "aforo", "disponible", "hay lugar", "hay mesa",
    "tienen mesa", "mesas disponibles", "cupos", "espacio"
]

def restaurant_router_node(state: RoutingState) -> RoutingState:
    """
    Router optimizado para restaurante: detecta intenciones relacionadas con 
    reservas basadas en aforo en lugar de servicios.
    """
    user_text = state.get("user_input", "").lower().strip()
    client_name = state.get("client_name", "cliente")
    
    if not user_text:
        return {
            "response_text": f"Hola {client_name}, ¿en qué puedo ayudarte con tu reserva?",
            "intent": Intent.GREETING,
        }

    # 1) Saludos
    if any(greeting in user_text for greeting in GREETINGS):
        return {
            "response_text": f"¡Hola {client_name}! ¿Para cuántas personas es tu reserva y para qué día?",
            "intent": Intent.GREETING,
        }

    # 2) Despedidas
    if any(farewell in user_text for farewell in FAREWELL_KEYWORDS):
        return {
            "response_text": f"¡Gracias por contactarnos {client_name}! Si necesitas algo más, aquí estoy.",
            "intent": Intent.FAREWELL,
        }

    # 3) Modificaciones (cancelar, cambiar, etc.)
    if any(mod in user_text for mod in MODIFICATION_KEYWORDS):
        return {
            "response_text": "Entiendo que quieres modificar tu reserva. Para ayudarte, necesito tu número de teléfono.",
            "intent": Intent.MODIFICATION_REQUEST,
        }

    # 4) Detección de tamaño de grupo (PARTY SIZE)
    # Buscamos números + "personas" o palabras relacionadas
    import re
    
    # Patrones como "4 personas", "para 3", "somos 5", etc.
    party_size_patterns = [
        r'(\d+)\s*(?:persona|personas|comensales|gente)',
        r'(?:para|somos|vamos)\s+(\d+)',
        r'(\d+)\s*(?:uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)',
        r'(?:uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+(?:persona|personas)'
    ]
    
    detected_party_size = None
    for pattern in party_size_patterns:
        match = re.search(pattern, user_text)
        if match:
            # Convertir números escritos a dígitos
            number_word = match.group(1) if match.groups() else match.group(0)
            try:
                detected_party_size = int(number_word)
                if 1 <= detected_party_size <= 20:  # Rango razonable
                    break
            except ValueError:
                # Mapear números escritos a dígitos
                word_to_num = {
                    'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
                    'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10
                }
                if number_word.lower() in word_to_num:
                    detected_party_size = word_to_num[number_word.lower()]
                    break

    # 5) Detección de fechas
    has_date_keywords = any(date_kw in user_text for date_kw in DATE_KEYWORDS)
    
    # 6) Detección de filtros de tiempo
    has_time_filter = any(tf in user_text for tf in TIME_FILTER_KEYWORDS)

    # Lógica de enrutamiento principal
    if detected_party_size:
        # Si detectamos tamaño de grupo, vamos a booking
        return {
            "response_text": f"¡Perfecto! Tienes mesa para {detected_party_size} personas. ¿Para qué día te gustaría reservar?",
            "intent": Intent.BOOKING,
            "detected_party_size": detected_party_size,
        }
    elif has_date_keywords or has_time_filter:
        # Si hay fecha o filtros de tiempo pero no tamaño de grupo
        return {
            "response_text": "¿Para cuántas personas sería la reserva?",
            "intent": Intent.BOOKING,
        }
    elif any(cap in user_text for cap in CAPACITY_KEYWORDS):
        # Consultas sobre capacidad/disponibilidad general
        return {
            "response_text": "Puedo revisar la disponibilidad. ¿Para cuántas personas y qué día necesitas la mesa?",
            "intent": Intent.BOOKING,
        }
    else:
        # Por defecto, asumimos que quiere hacer una reserva
        return {
            "response_text": f"Claro {client_name}, ¿para cuántas personas es tu reserva y para qué día?",
            "intent": Intent.BOOKING,
        }
