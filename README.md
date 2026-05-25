# 🏎️ F1 Tutor Bot

> Bot educativo de Fórmula 1 para Telegram, con inteligencia artificial, datos en vivo y reglamento oficial indexado.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)
![Groq](https://img.shields.io/badge/IA-Groq%20%2B%20Llama%203.3-orange)
![SQLite](https://img.shields.io/badge/SQLite-Historial%20%26%20Métricas-003B57?logo=sqlite&logoColor=white)
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

## 🏗️ Arquitectura del Proyecto

Este bot fue diseñado siguiendo los principios de **Arquitectura Limpia (Clean Architecture)**. La estructura del código busca la separación estricta de responsabilidades, garantizando que la lógica de negocio sea completamente agnóstica a la plataforma de mensajería, la base de datos y los proveedores de Inteligencia Artificial.

### 📐 Capas del Sistema

El proyecto se divide en tres capas fundamentales que respetan la regla de dependencia hacia el interior:

1. **Capa de Presentación (`src/presentation/`):** 
    Contiene los controladores (`RaceController`, `QuizController`, `SystemController`) encargados de recibir los estímulos de la interfaz de usuario y formatear las respuestas. No manejan lógica de negocio ni llamadas directas a APIs de datos.
   
2. **Capa de Casos de Uso / Negocio (`src/use_cases/`):**
   Es el núcleo de la aplicación. Aquí residen las reglas puras del sistema (`TutorUseCase` y `QuizUseCase`), como el procesamiento de consultas educativas o las mecánicas del juego de trivia. Esta capa es 100% reutilizable si el bot se migra a Discord, WhatsApp o una plataforma web.

3. **Capa de Infraestructura (`src/infrastructure/`):**
   Aloja las implementaciones de las herramientas y servicios externos. Esto incluye la persistencia en base de datos (`db.py`), la conexión con las APIs de F1 y clima, el motor RAG para el reglamento de la FIA, el servicio de transcripción de audio (Whisper) y el adaptador del Framework de mensajería (`telegram_bot.py`).

### 🏎️ Beneficios de este Diseño

* **Agnóstico a la plataforma:** Cambiar de Telegram a otra plataforma de mensajería requiere únicamente crear un nuevo adaptador en infraestructura e inyectarle los controladores existentes, sin tocar una sola línea de lógica de negocio.
* **Flexibilidad de proveedores de IA:** Los servicios de transcripción y modelos LLM están aislados. Si se decide migrar de Groq/Whisper a OpenAI o a un modelo local (Llama 3), el impacto se reduce a un solo archivo de infraestructura.
* **Alta Mantenibilidad:** El archivo de entrada `main.py` actúa estrictamente como un orquestador e inyector de dependencias minimalista, facilitando la escalabilidad del sistema y la creación de pruebas unitarias (`tests/`).

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
├── main.py                      # Punto de entrada agnóstico (orquestador del sistema)
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos y carpetas ignorados por Git
│
├── scripts/                     # Scripts utilitarios y herramientas de mantenimiento local
│   ├── ver_metricas.py          # Script para auditar consultas y analizar estadísticas
│   └── actualizar_cerebro.py    # Script de actualización dinámica del RAG mediante inyección de RSS
│
├── tests/                       # Pruebas automatizadas del sistema
│   └── test_f1_api.py           # Tests unitarios con Pytest para el conversor de horarios
│
└── src/                         # Código fuente y soporte del proyecto
    │
    ├── presentation/            # Controladores de interfaz de usuario
    │   ├── race_controller.py   # Despacho de estadísticas y datos en vivo
    │   ├── quiz_controller.py   # Control de comandos de la trivia
    │   └── system_controller.py # Manejo de mensajes de texto, audios con UUID y comandos globales
    │
    ├── use_cases/               # Casos de uso con las reglas puras de negocio
    │   ├── tutor_use_case.py    # Lógica de procesamiento de consultas del Tutor
    │   └── quiz_use_case.py     # Lógica y ciclo de juego del Quiz de F1
    │
    ├── img/                     # Recursos visuales y multimedia estáticos del proyecto
    │   └── f1bot_avatar.jpg     # Imagen de perfil / Avatar oficial del chatbot
    │
    └── infrastructure/          # CAPA DE HERRAMIENTAS: Servicios externos y persistencia
        ├── db.py                # Gestión del historial de usuarios en SQLite (Con consultas parametrizadas)
        ├── f1_api.py            # Cliente para la API de F1 en vivo (Jolpica)
        ├── f1_weather.py        # Conexión con OpenWeather API para datos climáticos
        ├── f1_knowledge.py      # Base de conocimiento estática de F1 2026
        ├── f1_rag.py            # Sistema RAG híbrido (Reglamento oficial FIA + Inyección dinámica de textos)
        ├── news_service.py      # Cliente extractor de feeds RSS para capturar la actualidad de la F1 en tiempo real
        ├── audio_service.py     # Transcripción de notas de voz con Whisper (Groq)
        ├── telegram_bot.py      # Adaptador y arranque específico de Telegram
        │
        └── reglamento_pdfs/     # Documentos oficiales de la FIA utilizados por el RAG
            ├── sporting.pdf     # Reglamento Deportivo (reglas de carrera, penalizaciones y formato de GP)
            ├── sporting_backup.pdf # Copia de respaldo para garantizar consistencia en la indexación
            └── technical.pdf    # Reglamento Técnico (especificaciones del motor, chasis y aerodinámica)

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

### 🔐 Seguridad Defensiva e Integridad

El sistema implementa medidas de protección avanzadas en cada una de sus capas para garantizar la estabilidad del servicio, mitigar abusos y proteger la privacidad:

* **Control de Abuso y Costos (Rate Limiting):** En la capa de presentación se analiza el flujo de entrada en memoria volátil. Si un usuario envía mensajes con una frecuencia menor a 2 segundos, el bot bloquea temporalmente la petición, cuidando las cuotas de consumo de las APIs de IA (Groq/Whisper).
* **Mitigación de Prompt Injection:** El *System Prompt* del modelo de lenguaje en el núcleo de negocio cuenta con directivas estrictas de aislamiento. Si un usuario intenta forzar al bot a salir de su rol o a revelar sus instrucciones internas, la IA esquiva el ataque de forma natural manteniendo su personalidad de tutor de F1.
* **Inmunidad contra Inyección SQL (SQLi):** Toda la persistencia local en SQLite utiliza consultas parametrizadas mediante placeholders (`?`). Ningún dato proveniente del usuario se concatena directamente en strings de bases de datos.
* **Concurrencia Segura y Limpieza de Temporales:** El procesamiento de notas de voz genera nombres de archivos unívocos mediante identificadores aleatorios (`uuid`), evitando colisiones por peticiones simultáneas. Además, el flujo está envuelto en bloques cerrados `try...finally`, asegurando que los archivos `.ogg` residuales se eliminen del disco local incluso ante fallas críticas del sistema.
* **Minimización de Datos y Privacidad:** El bot cumple con el principio de recopilación mínima (solo almacena el ID numérico e identifica usuarios sin alias como "Anónimo"). El comando `/reset` ejecuta un borrado físico y definitivo de los datos a petición del usuario.

---

## 🧪 Pruebas Automatizadas

El proyecto cuenta con una suite de pruebas unitarias automatizadas utilizando **Pytest** para garantizar que la lógica crítica (como la conversión de horarios de la F1 a zona local) funcione de manera correcta y no sufra regresiones.

Para ejecutar los tests en tu entorno local, simplemente corré el siguiente comando en la raíz del proyecto:

```
bash
python -m pytest
```

---

## 📊 Análisis de Métricas y Performance

El bot incluye un módulo de auditoría que permite analizar el comportamiento de los usuarios y la performance de la IA.

Cómo ejecutar el análisis:
Para obtener un reporte detallado (incluyendo latencia p95 y distribución de comandos), asegurate de tener pandas instalado y ejecutá:

```
Bash
python scripts/ver_metricas.py
```

Nota: Este script utiliza pandas para procesar los datos de uso almacenados en historial.db y generar insights accionables sobre el engagement y tiempos de respuesta.

⚙️ Arquitectura y Datos
Base de Datos: El proyecto utiliza sqlite3 para la auditoría de logs y ChromaDB para el almacenamiento vectorial.

Control de versiones: Por buenas prácticas, las carpetas de datos volátiles (como chroma_db/) están excluidas del control de versiones mediante .gitignore para garantizar un repositorio ligero y limpio.

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