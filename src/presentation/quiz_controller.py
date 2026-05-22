# src/presentation/quiz_controller.py
from telegram import Update
from telegram.ext import ContextTypes
from src.use_cases.quiz_use_case import QuizUseCase

class QuizController:
    """Controlador que maneja la interacción de comandos de la Trivia con Telegram."""
    
    def __init__(self, quiz_use_case: QuizUseCase):
        self.quiz_use_case = quiz_use_case
        self.emojis = {"facil": "🟢", "medio": "🟡", "dificil": "🔴"}

    async def cmd_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🏎️ ¡Bienvenido al Quiz de F1!\n\n"
            "Elegí la dificultad:\n"
            "🟢 /facil — Preguntas básicas\n"
            "🟡 /medio — Estrategia y reglamento\n"
            "🔴 /dificil — Datos técnicos avanzados"
        )

    async def iniciar_dificultad(self, update: Update, context: ContextTypes.DEFAULT_TYPE, dificultad: str):
        user_id = update.effective_user.id
        texto_pregunta = self.quiz_use_case.iniciar_juego(user_id, dificultad)
        
        await update.message.reply_text(
            f"{self.emojis[dificultad]} Dificultad: {dificultad.upper()}\n"
            f"5 preguntas. Respondé con A, B, C o D.\n\n"
            f"{texto_pregunta}"
        )

    async def cmd_facil(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "facil")

    async def cmd_medio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "medio")

    async def cmd_dificil(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.iniciar_dificultad(update, context, "dificil")