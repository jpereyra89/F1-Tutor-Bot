"""
main.py — Bot educativo de F1
Punto de entrada agnóstico e inicialización general del sistema.
"""

from dotenv import load_dotenv
load_dotenv()

import logging

# Infraestructura básica compartida
from src.infrastructure.db import init_db
from src.infrastructure.f1_rag import indexar_reglamento
from src.infrastructure.audio_service import AudioService

# Casos de Uso (Lógica de negocio pura)
from src.use_cases.quiz_use_case import QuizUseCase
from src.use_cases.tutor_use_case import TutorUseCase

# Capa de Presentación (Controladores)
from src.presentation.race_controller import RaceController
from src.presentation.quiz_controller import QuizController
from src.presentation.system_controller import SystemController

# Infraestructura específica de la plataforma de mensajería
from src.infrastructure.telegram_bot import TelegramBot

# Configuración del logger global del sistema
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. Inicialización de Casos de Uso y Servicios esenciales
quiz_use_case = QuizUseCase()
tutor_use_case = TutorUseCase()
audio_service = AudioService()

# 2. Inicialización de Controladores (Presentación)
race_controller = RaceController()
quiz_controller = QuizController(quiz_use_case)
system_controller = SystemController(tutor_use_case, quiz_use_case, audio_service)

# 3. Inicialización del Servidor de Mensajería (Telegram)
bot_service = TelegramBot(system_controller, race_controller, quiz_controller)


def main():
    # Inicialización física de recursos de datos e IA
    init_db()
    logging.info("📚 Indexando reglamento FIA 2026...")
    indexar_reglamento()

    # Encender los motores de la interfaz de usuario
    bot_service.encender()


if __name__ == "__main__":
    main()