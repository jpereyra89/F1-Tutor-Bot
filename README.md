# 🏎️ F1 Tutor Bot

> Bot educativo de Fórmula 1 para Telegram, con inteligencia artificial, datos en vivo y reglamento oficial indexado.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)
![Groq](https://img.shields.io/badge/IA-Groq%20%2B%20Llama%203.3-orange)
![OpenWeather](https://img.shields.io/badge/Clima-OpenWeather%20API-orange?logo=openweather&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-black?logo=chroma&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Pytest%20--%20Passing-brightgreen?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/Licencia-MIT-green)
![Costo](https://img.shields.io/badge/Costo-100%25%20Gratuito-brightgreen)

---

## ¿Qué es F1 Tutor?

**F1 Tutor** es un chatbot educativo sobre Fórmula 1 disponible en Telegram ([@f1tutor_bot](https://t.me/f1tutor_bot)).

Responde preguntas sobre reglamento, pilotos, circuitos, estrategias y resultados en tiempo real. Está diseñado para enseñar F1 de forma clara y entretenida, adaptándose al nivel del usuario — desde principiantes hasta fanáticos avanzados.

Desarrollado íntegramente en **Python**, sin licencias pagas.

---

## ✨ Funcionalidades

| Función | Descripción |
|---------|-------------|
| 🤖 **IA conversacional** | Responde cualquier pregunta sobre F1 con Groq + Llama 3.3 70B |
| 📡 **Datos en vivo** | Clasificaciones, resultados y próximas carreras via Jolpica API |
| 🌤️ **Clima en carrera** | Pronóstico meteorológico en tiempo real para los circuitos usando OpenWeather |
| 📚 **Reglamento FIA 2026** | 2490 fragmentos del reglamento oficial indexados con RAG (ChromaDB) |
| 🧠 **Base de conocimiento** | Circuitos, pilotos, escuderías y glosario técnico de la temporada 2026 |
| 🎙️ **Mensajes de voz** | Transcripción automática con Whisper via Groq |
| 💾 **Historial persistente** | Recuerda las conversaciones anteriores de cada usuario (SQLite) |
| 🎯 **Quiz de F1** | Preguntas en 3 niveles: Fácil, Medio y Difícil |
| 📊 **Auditoría y Métricas** | Registro local de consultas en SQLite para análisis de estadísticas y uso |

---

## 🤖 Comandos

| Comando | Descripción |
|---------|-------------|
| `/start` | Mensaje de bienvenida |
| `/standings` | Clasificación actual de pilotos |
| `/constructors` | Clasificación de constructores |
| `/lastrace` | Resultados de la última carrera |
| `/nextrace` | Próxima carrera del calendario |
| `/reglamento` | Estado del reglamento indexado |
| `/quiz` | Iniciar el quiz de F1 |
| `/facil` | Quiz nivel fácil |
| `/medio` | Quiz nivel medio |
| `/dificil` | Quiz nivel difícil |
| `/reset` | Borrar historial de conversación |

---

## 🛠️ Stack tecnológico

| Tecnología | Uso |
|------------|-----|
| Python 3.13 | Lenguaje principal |
| python-telegram-bot | Integración con Telegram |
| Groq + Llama 3.3 70B | Motor de IA |
| Whisper (via Groq) | Transcripción de audio |
| ChromaDB | Base de datos vectorial (RAG) |
| sentence-transformers | Embeddings para búsqueda semántica |
| Jolpica API | Datos en vivo de F1 (sin API key) |
| OpenWeather API | Datos meteorológicos en tiempo real para los circuitos |
| SQLite | Historial de conversaciones, auditoría y métricas locales |
| python-dotenv | Gestión de variables de entorno |

---

## 🚀 Instalación

### Requisitos previos
- Python 3.10 o superior
- [ffmpeg](https://ffmpeg.org/) instalado en el sistema
- Cuenta en [Telegram](https://telegram.org/)
- Cuenta en [Groq](https://console.groq.com/) (gratuita)
- Cuenta en [OpenWeather](https://openweathermap.org/) (gratuita)

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/jpereyra89/F1-Tutor-Bot.git
cd F1-Tutor-Bot
```

**2. Crear y activar el entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**

Creá un archivo `.env` en la raíz del proyecto:
```
TELEGRAM_TOKEN=tu_token_de_botfather
GROQ_API_KEY=tu_api_key_de_groq
OPENWEATHER_API_KEY=tu_api_key_de_openweather
```

- **TELEGRAM_TOKEN**: Obtenerlo hablando con [@BotFather](https://t.me/BotFather) en Telegram
- **GROQ_API_KEY**: Obtenerlo en [console.groq.com](https://console.groq.com) (gratis)
- **OPENWEATHER_API_KEY**: Obtenerlo en [openweather.org](https://openweathermap.org/) (gratis)

**5. Ejecutar el bot**
```bash
python main.py
```

La primera vez el bot va a descargar e indexar el reglamento oficial de la FIA automáticamente. Esto puede tardar unos minutos.

---

## 📁 Estructura del proyecto

```
F1-Tutor-Bot/
│
├── main.py                 # Archivo principal — handlers y lógica del bot de Telegram
├── ver_metricas.py         # Auditar consultas y analizar estadísticas
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos y carpetas ignorados por Git
│
├── tests/                  # Pruebas automatizadas del sistema
│   └── test_f1_api.py      # Tests unitarios con Pytest para el conversor de horarios
│
└── src/                    # Código fuente y soporte del proyecto
    │
    └── infrastructure/    # Infraestructura, servicios y base de conocimiento
        ├── db.py           # Gestión del historial de usuarios en SQLite
        ├── f1_api.py       # Cliente para la API de F1 en vivo (Jolpica)
        ├── f1_weather.py   # Conexión con OpenWeather API para datos climáticos en carrera
        ├── f1_knowledge.py # Base de conocimiento estática de F1 2026
        ├── f1_rag.py       # Sistema RAG para el reglamento oficial de la FIA
        │
        └── reglamento_pdfs/ # Documentos oficiales de la FIA utilizados por el RAG
            ├── sporting.pdf
            ├── sporting_backup.pdf
            └── technical.pdf

```

---

## 🔑 Obtener las API keys

### Telegram Token
1. Abrí Telegram y buscá [@BotFather](https://t.me/BotFather)
2. Mandá `/newbot` y seguí las instrucciones
3. Copiá el token que te da

### Groq API Key
1. Entrá a [console.groq.com](https://console.groq.com)
2. Creá una cuenta gratuita
3. En "API Keys" → "Create API Key"
4. Copiá la key (empieza con `gsk_...`)

### OpenWeather API Key
1. Entrá a [openweathermap.org](https://openweathermap.org/) y registrate para crear una cuenta gratuita
2. Una vez dentro de tu perfil, andá a la pestaña **"API keys"**
3. En el panel derecho, ponle un nombre a tu key (por ejemplo: `f1-bot`) y hacé clic en **"Generate"**
4. Copiá el código alfanumérico generado

---

## 🧪 Pruebas Automatizadas

El proyecto cuenta con una suite de pruebas unitarias automatizadas utilizando **Pytest** para garantizar que la lógica crítica (como la conversión de horarios de la F1 a zona local) funcione de manera correcta y no sufra regresiones.

Para ejecutar los tests en tu entorno local, simplemente corré el siguiente comando en la raíz del proyecto:

```
bash
python -m pytest
```

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Podés usarlo, modificarlo y distribuirlo libremente.

---

## 👤 Autor

**Jose Pereyra**
- GitHub: [@jpereyra89](https://github.com/jpereyra89)
- Email: josepereyra89@gmail.com
- Bot: [@f1tutor_bot](https://t.me/f1tutor_bot)

---

*Desarrollado con ❤️ y mucha pasión por la F1 🏎️💨🏁*