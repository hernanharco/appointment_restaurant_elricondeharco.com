# Agent Documentation

## Overview
Sistema de agentes inteligentes construido con LangGraph/LangSmith para automatizar procesos de negocio y manejar interacciones complejas con usuarios.

## Stack Tecnológico
- **Framework**: LangGraph
- **Orchestration**: LangSmith
- **Language Models**: Claude v1, ChatGPT
- **Memory System**: Persistencia de conversaciones
- **Tools**: Integraciones con APIs externas

## Estructura de Directorios

```
backend/app/agents/
├── core/                # Núcleo del sistema de agentes
├── formatters/          # Formateo de respuestas
├── memory/              # Sistema de memoria persistente
├── nodes/               # Nodos del grafo de agentes
├── routing/             # Lógica de enrutamiento
├── schemas/             # Schemas para agentes
├── shared/              # Componentes compartidos
├── tools/               # Herramientas y utilidades
├── utils/               # Funciones auxiliares
├── validators/          # Validación de inputs/outputs
├── contextClaudev1.md   # Configuración Claude
├── init_chatgpt.md      # Configuración ChatGPT
├── manualAgents.md      # Documentación manual
└── niveles.md           # Definición de niveles de agentes
```

## Componentes Principales

### core/
Núcleo del sistema de agentes:
- **Agent base classes**: Clases base para todos los agentes
- **Graph definitions**: Definición de grafos de LangGraph
- **State management**: Manejo de estado entre nodos
- **Configuration**: Configuración central de agentes

### memory/
Sistema de memoria persistente:
- **Session memory**: Memoria de sesión por usuario
- **Long-term memory**: Almacenamiento a largo plazo
- **Context retrieval**: Recuperación de contexto relevante
- **Memory cleanup**: Limpieza y mantenimiento

### nodes/
Nodos del grafo de agentes:
- **Intent detection**: Identificación de intenciones
- **Task execution**: Ejecución de tareas específicas
- **Decision making**: Toma de decisiones
- **Response generation**: Generación de respuestas

### routing/
Lógica de enrutamiento inteligente:
- **Intent routing**: Enrutamiento basado en intención
- **Load balancing**: Distribución de carga
- **Fallback handling**: Manejo de casos fallback
- **Priority queuing**: Colas de prioridad

### tools/
Herramientas disponibles para agentes:
- **API integrations**: Conexión con APIs externas
- **Database tools**: Herramientas de base de datos
- **File operations**: Manipulación de archivos
- **Web scraping**: Extracción de información web

### schemas/
Schemas para validación:
- **Input schemas**: Validación de entradas
- **Output schemas**: Estructura de salidas
- **State schemas**: Definición de estados
- **Message schemas**: Formato de mensajes

## Tipos de Agentes

### Niveles de Agentes (niveles.md)
1. **Level 1 - Basic**: Respuestas simples y directas
2. **Level 2 - Contextual**: Considera contexto de conversación
3. **Level 3 - Proactive**: Anticipa necesidades del usuario
4. **Level 4 - Autonomous**: Toma decisiones complejas
5. **Level 5 - Strategic**: Planificación estratégica

### Configuraciones Disponibles
- **Claude v1**: Configuración optimizada para Claude
- **ChatGPT**: Configuración para modelos OpenAI

## Flujo de Trabajo

### 1. Input Processing
```python
# Recepción y validación de input
user_input = validate_input(raw_input)
intent = detect_intent(user_input)
```

### 2. Memory Retrieval
```python
# Recuperación de contexto relevante
context = memory.retrieve_relevant(user_id, intent)
session_state = memory.get_session(user_id)
```

### 3. Agent Routing
```python
# Enrutamiento al agente apropiado
agent = routing.select_agent(intent, context, level)
```

### 4. Task Execution
```python
# Ejecución de la tarea
result = agent.execute(user_input, context, tools)
```

### 5. Response Generation
```python
# Generación de respuesta formateada
response = formatters.format_response(result, intent)
memory.update_session(user_id, response)
```

## Memory System

### Session Memory
- Almacenamiento temporal por sesión
- Contexto de conversación activa
- Estado de tareas en progreso

### Long-term Memory
- Preferencias de usuario
- Historial de interacciones
- Patrones de comportamiento

### Memory Cleanup
- Limpieza automática periódica
- Compresión de información antigua
- Eliminación de datos sensibles

## Tools Integration

### Available Tools
- **Database queries**: Consultas a base de datos
- **API calls**: Llamadas a APIs externas
- **File operations**: Lectura/escritura de archivos
- **Web search**: Búsqueda en internet
- **Calculations**: Operaciones matemáticas

### Tool Registration
```python
# Registro de nuevas herramientas
@register_tool
def custom_tool(input_data):
    # Lógica de la herramienta
    return result
```

## Configuration

### Agent Configuration
```python
agent_config = {
    "model": "claude-v1",
    "temperature": 0.7,
    "max_tokens": 2000,
    "tools": ["database", "api", "calculator"],
    "memory_enabled": True
}
```

### Environment Variables
- `LANGSMITH_API_KEY`: API key para LangSmith
- `CLAUDE_API_KEY`: API key para Claude
- `OPENAI_API_KEY`: API key para OpenAI
- `MEMORY_DB_URL`: URL para base de datos de memoria

## Development

### Creating New Agents
```python
class CustomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
    
    def execute(self, input_data, context):
        # Lógica del agente
        return self.process_task(input_data, context)
```

### Testing Agents
```python
def test_agent_behavior():
    agent = CustomAgent(test_config)
    result = agent.execute(test_input, test_context)
    assert result.expected_output
```

## Monitoring

### LangSmith Integration
- Tracking de ejecuciones
- Performance metrics
- Error analysis
- Usage analytics

### Logging
- Structured logging
- Performance metrics
- Error tracking
- Audit trails

## Security

### Input Validation
- Sanitización de inputs
- Validación de schemas
- Rate limiting
- Content filtering

### Data Protection
- Encriptación de datos sensibles
- Access control
- Audit logging
- Data retention policies

## Best Practices

1. **Single Responsibility**: Cada agente tiene una responsabilidad clara
2. **Stateless Design**: Agentes no mantienen estado interno
3. **Error Handling**: Manejo robusto de errores
4. **Memory Management**: Uso eficiente de memoria
5. **Tool Validation**: Validación estricta de herramientas
6. **Testing**: Cobertura completa de tests
7. **Documentation**: Documentación clara y actualizada

## Troubleshooting

### Common Issues
- **Memory overflow**: Limpiar memoria periódicamente
- **Tool failures**: Validar conectividad de herramientas
- **Performance**: Optimizar prompts y reducir tokens
- **Routing errors**: Revisar lógica de enrutamiento

### Debug Mode
```python
# Habilitar debug mode
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
TRACE_EXECUTION = True
```
