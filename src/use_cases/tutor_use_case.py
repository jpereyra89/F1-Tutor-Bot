# src/use_cases/tutor_use_case.py

import os
from groq import Groq
from src.infrastructure.f1_knowledge import F1_STATIC_KNOWLEDGE
from src.infrastructure.db import cargar_historial, guardar_historial
from src.infrastructure.f1_api import get_relevant_f1_data
from src.infrastructure.f1_rag import buscar_reglamento

class TutorUseCase:
    """Caso de uso que coordina la IA para responder como un profesor de F1,
    enriqueciendo la consulta con RAG y APIs en vivo, y limpiando la salida.
    """
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.max_historial = 20
        self.system_prompt = f"""
Sos un experto y apasionado profesor de Fórmula 1. Tu objetivo es enseñar de forma natural, fluida y con entusiasmo.

REGLAS CRÍTICAS DE ESTO (SÉ NATURAL):
1. Hablá SIEMPRE en primera persona, como un humano real que sabe todo esto de memoria gracias a años de experiencia.
2. Está TERMINANTEMENTE PROHIBIDO hacer referencias a textos externos, bases de datos o al contexto. 
   - Prohibido decir: "según los datos", "como se menciona en...", "en la base de conocimiento", "según el fragmento", "el texto indica".
   - En lugar de decir: "Esto se menciona en la base de conocimiento donde dice que Lando ganó", simplemente decí: "¡Lando Norris se coronó campeón en una temporada increíble!".
3. Si la información extra que recibís ([DATOS EN VIVO] o reglamento) no responde directamente a la pregunta o viene vacía, usá tu conocimiento general de forma natural o admití amigablemente que no tenés el dato exacto de la FIA a mano, pero nunca expongas cómo funciona el sistema por dentro.

CÓMO ENSEÑAR:
- Si el alumno es principiante: usá analogías simples y evitá jerga técnica sin explicar.
- Si el alumno tiene conocimiento: podés profundizar en estrategia, reglamento técnico, datos.
- Siempre que puedas, conectá los conceptos con ejemplos reales de carreras o pilotos.
- Usá emojis con moderación para hacer la conversación más dinámica 🏎️.
- Respondé en español, de forma clara y concisa.

BASE DE CONOCIMIENTO INTERNA:
{F1_STATIC_KNOWLEDGE}
"""
        # Filtros de expresiones por si las dudas el modelo se olvida de la regla
        self.frases_prohibidas = [
            "según los datos proporcionados", "según los datos en vivo",
            "según la información proporcionada", "según mi conocimiento general",
            "en los fragmentos proporcionados", "en las páginas proporcionadas",
            "no se menciona en los fragmentos", "no hay información en los fragmentos",
            "la información proporcionada", "en el contexto proporcionado",
            "según el contexto", "base de conocimiento proporcionada",
            "en las páginas que se mencionan", "en el texto proporcionado",
            "no se menciona en el texto", "no se menciona el número",
        ]

    async def ejecutar_consulta(self, user_id: int, mensaje_usuario: str) -> str:
        """Coordina todo el flujo de recopilación de datos, llamada a Groq y limpieza de respuesta."""
        
        # 1. Buscar datos en vivo si aplica
        datos_vivos = await get_relevant_f1_data(mensaje_usuario)

        # 2. Buscar en el reglamento oficial (RAG) mediante palabras clave
        palabras_reglamento = [
            "reglamento", "regla", "artículo", "norma", "permitido", "prohibido",
            "sanción", "penalización", "peso", "dimensión", "motor", "combustible",
            "neumático", "alerón", "drs", "ers", "mgu", "pit", "boxes", "parc fermé",
            "bandera", "safety car", "vsc", "descalificación", "protesta"
        ]
        
        datos_reglamento = ""
        if any(w in mensaje_usuario.lower() for w in palabras_reglamento):
            datos_reglamento = buscar_reglamento(mensaje_usuario)

        # 3. Construir mensaje enriquecido para el contexto de la IA
        extras = ""
        if datos_vivos:
            extras += f"\n\n[DATOS EN VIVO]\n{datos_vivos}\n[/DATOS EN VIVO]"
        if datos_reglamento:
            extras += f"\n\n{datos_reglamento}"

        mensaje_enriquecido = mensaje_usuario + extras
        
        # 4. Manejar el historial de conversación (Carga, añade usuario, guarda)
        mensajes = self._armar_contexto_contextual(user_id, mensaje_enriquecido)

        # 5. Petición a Groq LLM
        respuesta_raw = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensajes,
            max_tokens=1024,
            temperature=0.7,
        )
        texto_respuesta = respuesta_raw.choices[0].message.content

        # 6. Guardar la respuesta del asistente en el historial
        self._guardar_asistente_en_historial(user_id, texto_respuesta)

        # 7. Aplicar limpieza profunda de textos prohibidos (Post-procesamiento)
        return self._limpiar_texto(texto_respuesta)

    def _armar_contexto_contextual(self, user_id: int, mensaje_enriquecido: str) -> list[dict]:
        historial = cargar_historial(user_id)
        historial.append({"role": "user", "content": mensaje_enriquecido})
        guardar_historial(user_id, historial)
        return [{"role": "system", "content": self.system_prompt}] + historial[-self.max_historial:]

    def _guardar_asistente_en_historial(self, user_id: int, respuesta: str):
        historial = cargar_historial(user_id)
        historial.append({"role": "assistant", "content": respuesta})
        guardar_historial(user_id, historial)

    def _limpiar_texto(self, texto: str) -> str:
        """Remueve muletillas de LLM de forma interna."""
        for frase in self.frases_prohibidas:
            texto = texto.replace(frase, "")
        texto = texto.replace("Sin embargo, ,", "Sin embargo,")
        return texto.strip()