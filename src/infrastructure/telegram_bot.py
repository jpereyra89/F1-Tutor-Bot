# src/infrastructure/telegram_bot.py
import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

class TelegramBot:
    """Encapsula la infraestructura específica de Telegram para aislar el main.py."""
    
    def __init__(self, system_controller, race_controller, quiz_controller):
        # El token se lee ACÁ, donde pertenece (Infraestructura de Telegram)
        self.token = os.environ.get("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("Falta la variable de entorno TELEGRAM_TOKEN")
            
        self.system_controller = system_controller
        self.race_controller = race_controller
        self.quiz_controller = quiz_controller
        self.app = None

    def inicializar(self):
        """Configura la aplicación y conecta los controladores de presentación."""
        self.app = ApplicationBuilder().token(self.token).build()

        # Rutas del Controlador de Sistema
        self.app.add_handler(CommandHandler("start",      self.system_controller.cmd_start))
        self.app.add_handler(CommandHandler("reglamento", self.system_controller.cmd_reglamento))
        self.app.add_handler(CommandHandler("reset",      self.system_controller.cmd_reset))
        
        # Rutas del Controlador de Estadísticas de Carrera
        self.app.add_handler(CommandHandler("standings",    self.race_controller.cmd_standings))
        self.app.add_handler(CommandHandler("constructors", self.race_controller.cmd_constructors))
        self.app.add_handler(CommandHandler("lastrace",     self.race_controller.cmd_lastrace))
        self.app.add_handler(CommandHandler("nextrace",     self.race_controller.cmd_nextrace))
        
        # Rutas del Controlador del Quiz
        self.app.add_handler(CommandHandler("quiz",    self.quiz_controller.cmd_quiz))
        self.app.add_handler(CommandHandler("facil",   self.quiz_controller.cmd_facil))
        self.app.add_handler(CommandHandler("medio",   self.quiz_controller.cmd_medio))
        self.app.add_handler(CommandHandler("dificil", self.quiz_controller.cmd_dificil))
        
        # Manejo de Textos Libres y Notas de Voz
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.system_controller.manejar_mensaje))
        self.app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, self.system_controller.manejar_audio))

    def encender(self):
        """Lanza el bot en modo polling."""
        if not self.app:
            self.inicializar()
        logging.info("🏎️ Bot de Telegram iniciado y escuchando...")
        self.app.run_polling()