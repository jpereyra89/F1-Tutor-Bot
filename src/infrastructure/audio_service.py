# src/infrastructure/audio_service.py

import os
from groq import Groq

class AudioService:
    """Servicio de infraestructura encargado de la transcripción de audio mediante Whisper."""
    
    def __init__(self):
        # Inicializa su propio cliente de infraestructura aislado
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])

    async def transcribir_ogg(self, file_path: str) -> str:
        """Toma un archivo local en formato .ogg y devuelve su transcripción en texto."""
        with open(file_path, "rb") as f:
            transcripcion = self.client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f,
                language="es",
            )
        return transcripcion.text