# src/use_cases/quiz_use_case.py

from typing import Dict
from src.domain.quiz import QuizSession

class QuizUseCase:
    """Coordina las acciones de la trivia aislando la lógica de la interfaz de usuario."""
    
    def __init__(self):
        # Mantenemos las sesiones activas indexadas por el ID de usuario
        self._sesiones: Dict[int, QuizSession] = {}

    def iniciar_juego(self, user_id: int, dificultad: str) -> str:
        """Crea una nueva partida y devuelve la primera pregunta formateada."""
        try:
            sesion = QuizSession(dificultad)
            self._sesiones[user_id] = sesion
            return self._formatear_pregunta_actual(sesion)
        except ValueError as e:
            return f"❌ {str(e)}"

    def esta_jugando(self, user_id: int) -> bool:
        """Verifica si el usuario tiene una partida en curso."""
        return user_id in self._sesiones

    def responder(self, user_id: int, respuesta: str) -> str:
        """Procesa el intento del alumno y devuelve el resultado con la explicación."""
        if not self.esta_jugando(user_id):
            return "❌ No tenés ninguna partida activa. Escribí /quiz para empezar."

        sesion = self._sesiones[user_id]
        resp = respuesta.strip().upper()
        letras_validas = ["A", "B", "C", "D"]

        if resp not in letras_validas:
            return "Respondé con A, B, C o D 👀"

        # Evaluamos usando la entidad de dominio pura
        es_correcta, pregunta = sesion.procesar_respuesta(resp)
        letras = ["A", "B", "C", "D"]
        
        # Armamos el bloque de feedback de la respuesta
        if es_correcta:
            resultado = f"✅ ¡Correcto!\n\nKit de aprendizaje 📖: {pregunta['exp']}"
        else:
            opcion_correcta_texto = pregunta["ops"][letras.index(pregunta["r"])]
            resultado = f"❌ Incorrecto. La respuesta era {pregunta['r']}) {opcion_correcta_texto}\n\nKit de aprendizaje 📖: {pregunta['exp']}"

        # Si terminó el juego, calculamos el cierre y eliminamos la sesión
        if sesion.pregunta_terminada:
            puntaje = sesion.puntaje
            total = sesion.total_preguntas
            del self._sesiones[user_id]
            
            emoji = "🏆" if puntaje == total else "🎯" if puntaje >= total // 2 else "📚"
            mensaje_final = (
                f"{resultado}\n\n"
                f"{'—' * 20}\n"
                f"{emoji} ¡Quiz terminado!\n"
                f"Tu récord: {puntaje}/{total}\n\n"
            )
            if puntaje == total:
                mensaje_final += "¡Sos un experto absoluto en F1! 🏎️"
            elif puntaje >= total // 2:
                mensaje_final += "Seguí practicando, ¡vas por excelente camino! 💪"
            else:
                mensaje_final += "Te queda reglamento por leer, ¡pero vas por buen camino! 📚"
                
            return mensaje_final

        # Si quedan preguntas, le pegamos la siguiente abajo
        return f"{resultado}\n\n{self._formatear_pregunta_actual(sesion)}"

    def _formatear_pregunta_actual(self, sesion: QuizSession) -> str:
        """Método interno privado para armar el texto estético de la pregunta."""
        pregunta = sesion.obtener_pregunta_actual()
        letras = ["A", "B", "C", "D"]
        
        texto = f"❓ Pregunta {sesion.actual + 1}/{sesion.total_preguntas}\n\n{pregunta['p']}\n\n"
        for letra, opcion in zip(letras, pregunta["ops"]):
            texto += f"{letra}) {opcion}\n"
        return texto