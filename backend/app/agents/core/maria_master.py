import logging
from typing import Dict, Any

from app.agents.routing.graph import graph
from app.agents.core.thread_manager import ThreadManager
from app.db.session import SessionLocal
from app.agents.memory.memory_orchestrator import MemoryOrchestrator

logger = logging.getLogger(__name__)

_THREAD_VERSION = "v3"


class MariaMaster:

    async def process_message(self, phone: str, user_input: str) -> Dict[str, Any]:
        thread_id = ThreadManager.build_thread_id(phone + _THREAD_VERSION)

        db = SessionLocal()
        memory = MemoryOrchestrator(db)

        try:
            memory.store_user_message(phone, user_input)
            _, memory_context = memory.build_context(phone, user_input)

            payload = {
                "messages": [{"role": "user", "content": user_input}],
                "client_phone": phone,
                "memories": memory_context,
            }

            config = {"configurable": {"thread_id": thread_id}}

            state = await graph.ainvoke(payload, config=config)

            ai_text = self._extract_response_text(state)
            memory.store_ai_message(phone, ai_text)

            return {"text": ai_text}

        except Exception:
            logger.exception("Graph invocation error")
            return {"text": "Ups, hubo un problema procesando tu mensaje."}

        finally:
            db.close()

    def _extract_response_text(self, state: dict) -> str:
        if not state:
            return "No pude generar respuesta."

        # ainvoke directo devuelve el state sin wrapper "values"
        response_text = state.get("response_text")
        if response_text:
            return response_text

        messages = state.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                return msg.get("content", "")
            if hasattr(msg, "type") and msg.type == "ai":
                return msg.content

        return "No pude generar respuesta."


maria_master = MariaMaster()