"""
main.py — Bot educativo de F1
Punto de entrada agnóstico e inicialización general del sistema.
"""

from dotenv import load_dotenv
load_dotenv()

import logging
import re

# 1. Configuración de Seguridad para Logs (Filtro de Token)
class TelegramTokenFilter(logging.Filter):
    """Filtra el token del bot de los logs para que no aparezca en pantalla."""
    def filter(self, record):
        msg = record.getMessage()
        # Oculta el token en las URLs de las peticiones HTTP
        record.msg = re.sub(r'bot[a-zA-Z0-9_\-]+', 'bot[TOKEN_OCULTO]', msg)
        return True

# Configuración del logger global
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
httpx_logger = logging.getLogger("httpx")
httpx_logger.addFilter(TelegramTokenFilter())

# 2. Importaciones de la Arquitectura
from src.infrastructure.db import init_db
from src.infrastructure.f1_rag import indexar_reglamento
from src.infrastructure.audio_service import AudioService

from src.use_cases.quiz_use_case import QuizUseCase
from src.use_cases.tutor_use_case import TutorUseCase

from src.presentation.race_controller import RaceController
from src.presentation.quiz_controller import QuizController
from src.presentation.system_controller import SystemController

from src.infrastructure.telegram_bot import TelegramBot

# 3. Inicialización de Componentes
quiz_use_case = QuizUseCase()
tutor_use_case = TutorUseCase()
audio_service = AudioService()

race_controller = RaceController()
quiz_controller = QuizController(quiz_use_case)
system_controller = SystemController(tutor_use_case, quiz_use_case, audio_service)

bot_service = TelegramBot(system_controller, race_controller, quiz_controller)

def main():
    # Inicialización física de recursos de datos e IA
    init_db()
    
    logging.info("📚 Indexando reglamento FIA 2026 y preparando sistema...")
    # Esto indexa los PDFs de la carpeta 'reglamento_pdfs'
    indexar_reglamento()

    # Encender el bot
    logging.info("🚀 Motor encendido: F1 Tutor Bot listo en Telegram.")
    bot_service.encender()

if __name__ == "__main__":
    main()