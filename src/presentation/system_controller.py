# src/presentation/system_controller.py
import os
import logging
import time  # 🔐 Necesario para medir el tiempo entre mensajes
from telegram import Update
from telegram.ext import ContextTypes
from src.infrastructure.f1_rag import reglamento_disponible
from src.infrastructure.db import borrar_historial, registrar_consulta

class SystemController:
    """Controlador que maneja comandos globales, interacciones de texto y mensajería de voz con seguridad."""
    
    def __init__(self, tutor_use_case, quiz_use_case, audio_service):
        self.tutor_use_case = tutor_use_case
        self.quiz_use_case = quiz_use_case
        self.audio_service = audio_service
        
        # 🔐 Memoria volátil para el Rate Limiting (user_id: timestamp_ultimo_mensaje)
        self._ultimas_consultas = {}
        self._TIEMPO_MINIMO = 2.0  # Segundos mínimos entre interacciones

    def _es_spammer(self, user_id: int) -> bool:
        """🔐 Verifica si el usuario está enviando mensajes demasiado rápido."""
        ahora = time.time()
        ultimo_registro = self._ultimas_consultas.get(user_id, 0)
        
        if ahora - ultimo_registro < self._TIEMPO_MINIMO:
            return True  # Abuso detectado
            
        self._ultimas_consultas[user_id] = ahora
        return False

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        rag_status = "✅ Reglamento FIA indexado" if reglamento_disponible() else "⏳ Indexando reglamento..."
        await update.message.reply_text(
            "🏎️ ¡Bienvenido al Bot educativo de F1!\n\n"
            "Podés preguntarme lo que quieras sobre Fórmula 1:\n"
            "• Reglamento técnico y deportivo\n"
            "• Pilotos y escuderías\n"
            "• Circuitos y estrategias\n"
            "• Clasificaciones y resultados en vivo\n\n"
            f"Estado: {rag_status}\n\n"
            "Comandos disponibles:\n"
            "/standings — Clasificación de pilotos\n"
            "/constructors — Clasificación de constructores\n"
            "/lastrace — Resultado de la última carrera\n"
            "/nextrace — Próxima carrera\n"
            "/reglamento — Estado del reglamento indexado\n"
            "/quiz — Poné a prueba tus conocimientos de F1\n"
            "/reset — Borrar historial de conversación\n\n"
            "¿Por dónde empezamos? 🏁"
        )

    async def cmd_reglamento(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if reglamento_disponible():
            await update.message.reply_text(
                "✅ El reglamento oficial FIA 2026 está indexado y disponible.\n"
                "Preguntame cualquier duda sobre las reglas y busco directamente en el documento oficial."
            )
        else:
            await update.message.reply_text(
                "⏳ El reglamento todavía se está indexando. Intentá de nuevo en unos minutos."
            )

    async def cmd_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # 🔐 Cumplimiento de Privacidad: Eliminación total a petición del usuario
        borrar_historial(update.effective_user.id)
        await update.message.reply_text("✅ Historial borrado. ¡Volvemos a la largada!")

    async def manejar_mensaje(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username  # 🔐 Minimización de datos (no guardamos nombres reales)
        texto = update.message.text
        
        # 🔐 Control de abuso (Rate Limiting)
        if self._es_spammer(user_id):
            await update.message.reply_text("⚠️ ¡Boxes llenos! Por favor, esperá unos segundos antes de enviar otro mensaje.")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            if self.quiz_use_case.esta_jugando(user_id):
                resultado = self.quiz_use_case.responder(user_id, texto)
                registrar_consulta(user_id, username, texto, "quiz_respuesta")
                await update.message.reply_text(resultado)
                return

            respuesta = await self.tutor_use_case.ejecutar_consulta(user_id, texto)
            registrar_consulta(user_id, username, texto, "consulta_general")
            
            for i in range(0, len(respuesta), 4096):
                await update.message.reply_text(respuesta[i:i + 4096])
                
        except Exception as e:
            logging.error(f"Error en manejar_mensaje: {e}")
            await update.message.reply_text("⚠️ Error técnico. Intentá de nuevo.")

    async def manejar_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        # 🔐 Control de abuso en audios (son procesos pesados para la API de Whisper)
        if self._es_spammer(user_id):
            await update.message.reply_text("⚠️ ¡Boxes llenos! Esperá unos segundos antes de mandar otro audio.")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        try:
            voice = update.message.voice or update.message.audio
            file = await context.bot.get_file(voice.file_id)
            path = f"audio_{user_id}.ogg"
            await file.download_to_drive(path)
            
            texto = await self.audio_service.transcribir_ogg(path)
            os.remove(path)
            await update.message.reply_text(f"🎙️ Escuché: _{texto}_", parse_mode="Markdown")
            
            respuesta = await self.tutor_use_case.ejecutar_consulta(user_id, texto)
            registrar_consulta(user_id, username, texto, "consulta_general_audio")
            
            for i in range(0, len(respuesta), 4096):
                await update.message.reply_text(respuesta[i:i + 4096])
        except Exception as e:
            logging.error(f"Error en audio: {e}")
            await update.message.reply_text("⚠️ No pude procesar el audio.")