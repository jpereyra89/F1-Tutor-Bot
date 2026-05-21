"""
main.py — Bot educativo de F1 para Telegram
Combina base de conocimiento estática + datos en vivo + RAG sobre reglamento FIA 2026
"""

from dotenv import load_dotenv
load_dotenv()

import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from infraestructure.db import init_db, cargar_historial, guardar_historial, borrar_historial

from infraestructure.f1_knowledge import F1_STATIC_KNOWLEDGE
from infraestructure.f1_api import (
    get_relevant_f1_data,
    get_driver_standings,
    get_constructor_standings,
    get_last_race_results,
    get_next_race,
)
from infraestructure.f1_rag import buscar_reglamento, indexar_reglamento, reglamento_disponible

# --- Configuración ---
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_API_KEY   = os.environ["GROQ_API_KEY"]

SYSTEM_PROMPT = f"""
Sos un experto y apasionado profesor de Fórmula 1.

REGLA ABSOLUTA SOBRE CÓMO RESPONDER:
Respondé SIEMPRE como un experto humano que sabe las cosas de memoria.
EJEMPLO DE RESPUESTA INCORRECTA: "Según los fragmentos proporcionados, el peso mínimo..."
EJEMPLO DE RESPUESTA CORRECTA: "El peso mínimo del auto en 2026 es de 768 kg con piloto."
EJEMPLO DE RESPUESTA INCORRECTA: "No hay información en los fragmentos sobre ese tema."
EJEMPLO DE RESPUESTA CORRECTA: "El reglamento no especifica ese detalle, pero..."
Está TERMINANTEMENTE PROHIBIDO usar frases como: "según los datos proporcionados",
"en los fragmentos", "según el contexto", "la información proporcionada",
"no se menciona en los fragmentos", "según la base de conocimiento".

CÓMO ENSEÑAR:
- Si el alumno es principiante: usá analogías simples y evitá jerga técnica sin explicar.
- Si el alumno tiene conocimiento: podés profundizar en estrategia, reglamento técnico, datos.
- Siempre que puedas, conectá los conceptos con ejemplos reales de carreras o pilotos.
- Usá emojis con moderación para hacer la conversación más dinámica 🏎️.
- Respondé en español, de forma clara y concisa.

CUANDO TE PREGUNTEN DATOS EN VIVO (clasificaciones, resultados, próxima carrera):
- Se te proveerá contexto con datos actualizados entre [DATOS EN VIVO].
- Usá esos datos como fuente primaria y explicálos con contexto educativo.
- NUNCA uses frases como "según los datos proporcionados", "según los datos en vivo",
  "según la información que tengo", "en los fragmentos proporcionados" o similares.
  Respondé directamente como si supieras la respuesta de memoria.

CUANDO TE PREGUNTEN SOBRE EL REGLAMENTO:
- Se te proveerá el texto oficial de la FIA entre [REGLAMENTO OFICIAL FIA 2026].
- Respondé siempre de forma directa y natural, como si fueras un experto que sabe
  la respuesta de memoria. JAMÁS digas "en los fragmentos", "en el texto proporcionado",
  "no se menciona en los fragmentos", "según el contexto" ni ninguna variante.
- Si la info está en el reglamento usála. Si no está, respondé con tu conocimiento
  general. En ambos casos respondé igual de directo, sin aclarar de dónde viene la info.

BASE DE CONOCIMIENTO DE F1:
{F1_STATIC_KNOWLEDGE}
"""

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

conversaciones: dict[int, list[dict]] = {}
MAX_HISTORIAL = 20

# --- QUIZ ---

PREGUNTAS = {
    "facil": [
        {"p": "¿Cuántos puntos vale ganar una carrera?", "ops": ["20", "25", "30", "15"], "r": "B", "exp": "El ganador se lleva 25 puntos. El sistema va 25-18-15-12-10-8-6-4-2-1."},
        {"p": "¿Cuántos equipos hay en la F1 2026?", "ops": ["10", "12", "11", "9"], "r": "C", "exp": "En 2026 son 11 equipos: se sumaron Audi y Cadillac."},
        {"p": "¿Qué reemplaza al DRS en 2026?", "ops": ["ERS", "MGU-K", "Active Aero", "Boost Mode"], "r": "C", "exp": "El Active Aero usa alerones móviles que se abren en recta y se cierran en curva."},
        {"p": "¿Cuál es el circuito más largo del calendario 2026?", "ops": ["Monza", "Silverstone", "Spa-Francorchamps", "Bakú"], "r": "C", "exp": "Spa-Francorchamps mide 7.004 km, el más largo de la parrilla."},
        {"p": "¿Qué piloto argentino corre en 2026?", "ops": ["Sainz", "Colapinto", "Alonso", "Piastri"], "r": "B", "exp": "Franco Colapinto corre para Alpine en la temporada 2026."},
        {"p": "¿Quién es el campeón defensor en 2026?", "ops": ["Verstappen", "Hamilton", "Norris", "Leclerc"], "r": "C", "exp": "Lando Norris ganó el campeonato de pilotos 2025."},
        {"p": "¿En qué equipo corre Lewis Hamilton en 2026?", "ops": ["Mercedes", "Ferrari", "Red Bull", "McLaren"], "r": "B", "exp": "Hamilton se fue de Mercedes a Ferrari para la temporada 2025-2026."},
        {"p": "¿Cuántas vueltas tiene Mónaco aproximadamente?", "ops": ["53", "65", "78", "70"], "r": "C", "exp": "Mónaco tiene 78 vueltas porque el circuito es muy corto: solo 3.337 km."},
    ],
    "medio": [
        {"p": "¿Qué es el undercut en F1?", "ops": ["Adelantar por fuera", "Parar antes que el rival para sacarle ventaja con neumáticos frescos", "Usar el DRS en curva", "Salir último en boxes"], "r": "B", "exp": "El undercut consiste en entrar al pit antes que el rival para atacarlo con neumáticos frescos mientras él sigue en pista."},
        {"p": "¿Cuál es el peso mínimo del auto en 2026?", "ops": ["800 kg", "780 kg", "768 kg", "750 kg"], "r": "C", "exp": "El peso mínimo en 2026 es 768 kg con piloto, 32 kg menos que en 2025."},
        {"p": "¿Qué significa VSC?", "ops": ["Very Safe Car", "Virtual Safety Car", "Vehicle Speed Control", "Validated Speed Check"], "r": "B", "exp": "El VSC (Virtual Safety Car) obliga a todos los pilotos a reducir velocidad sin necesidad de desplegar el auto de seguridad físico."},
        {"p": "¿Cuántos motores puede usar un piloto por temporada?", "ops": ["3", "5", "4", "6"], "r": "C", "exp": "Cada piloto tiene 4 unidades de potencia por temporada. Si supera ese límite recibe penalización en la grilla."},
        {"p": "¿Qué motor usa Aston Martin en 2026?", "ops": ["Mercedes", "Ferrari", "Honda", "Ford"], "r": "C", "exp": "Honda se fue de Red Bull y en 2026 es proveedor exclusivo de Aston Martin."},
        {"p": "¿Qué circuito debuta en el calendario 2026?", "ops": ["Miami", "Las Vegas", "Madrid", "Singapur"], "r": "C", "exp": "Madrid debuta en 2026 con un circuito urbano callejero en el IFEMA."},
        {"p": "¿Qué es el parc fermé?", "ops": ["Zona de adelantamiento", "Período sin cambios al auto desde qualy hasta carrera", "Área de boxes", "Zona de penalizaciones"], "r": "B", "exp": "En parc fermé los equipos no pueden realizar cambios significativos al auto entre la clasificación y la carrera."},
        {"p": "¿Cuántos sprints hay en la temporada 2026?", "ops": ["4", "5", "6", "3"], "r": "C", "exp": "En 2026 hay 6 fines de semana sprint: China, Canadá, Austria, EEUU, Países Bajos y Singapur."},
    ],
    "dificil": [
        {"p": "¿Cuántos kW tiene el MGU-K en 2026?", "ops": ["120 kW", "200 kW", "350 kW", "500 kW"], "r": "C", "exp": "El MGU-K triplicó su potencia en 2026, pasando de 120 kW a 350 kW, representando ~50% de la potencia total."},
        {"p": "¿A qué velocidad el Super-Clipping recorta la potencia eléctrica?", "ops": ["250 km/h", "270 km/h", "290 km/h", "310 km/h"], "r": "C", "exp": "Por encima de 290 km/h el Super-Clipping reduce progresivamente la potencia eléctrica para ahorrar energía."},
        {"p": "¿Cuánto bajó la resistencia aerodinámica en 2026 respecto a 2025?", "ops": ["20%", "30%", "40%", "50%"], "r": "C", "exp": "La resistencia aerodinámica bajó un 40% gracias al Active Aero y el nuevo diseño del chasis."},
        {"p": "¿Cuál es el Cost Cap en 2026?", "ops": ["$135M", "$175M", "$215M", "$250M"], "r": "C", "exp": "El Cost Cap subió a $215 millones en 2026 para cubrir los mayores costos del nuevo reglamento."},
        {"p": "¿Cuántos mm menos mide el ancho del auto en 2026 vs 2025?", "ops": ["50 mm", "100 mm", "150 mm", "200 mm"], "r": "B", "exp": "Los autos 2026 son 100 mm más angostos: 1900 mm vs 2000 mm de 2025."},
        {"p": "¿Qué fabricante vuelve a la F1 en 2026 como proveedor de motores con Red Bull?", "ops": ["BMW", "Ford", "Volkswagen", "Renault"], "r": "B", "exp": "Ford vuelve a la F1 en 2026 como co-desarrollador de la unidad de potencia de Red Bull Powertrains."},
        {"p": "¿Cuántos fragmentos del reglamento FIA tiene indexados este bot?", "ops": ["1000", "1500", "2490", "3000"], "r": "C", "exp": "El bot indexó 2490 fragmentos del reglamento oficial FIA 2026 usando RAG con ChromaDB."},
    ]
}

# Estado del quiz por usuario
quiz_estado: dict[int, dict] = {}


def iniciar_quiz(user_id: int, dificultad: str):
    preguntas = PREGUNTAS[dificultad].copy()
    random.shuffle(preguntas)
    quiz_estado[user_id] = {
        "dificultad": dificultad,
        "preguntas":  preguntas[:5],  # 5 preguntas por quiz
        "actual":     0,
        "puntaje":    0,
    }


def pregunta_actual(user_id: int) -> str:
    estado = quiz_estado[user_id]
    idx    = estado["actual"]
    total  = len(estado["preguntas"])
    q      = estado["preguntas"][idx]
    ops    = q["ops"]
    letras = ["A", "B", "C", "D"]
    texto  = f"❓ Pregunta {idx + 1}/{total}\n\n{q['p']}\n\n"
    for l, o in zip(letras, ops):
        texto += f"{l}) {o}\n"
    return texto


def responder_quiz(user_id: int, respuesta: str) -> str:
    estado  = quiz_estado[user_id]
    idx     = estado["actual"]
    q       = estado["preguntas"][idx]
    letras  = ["A", "B", "C", "D"]
    total   = len(estado["preguntas"])
    resp    = respuesta.strip().upper()

    if resp not in letras:
        return "Respondé con A, B, C o D 👀"

    correcto = resp == q["r"]
    if correcto:
        estado["puntaje"] += 1
        resultado = f"✅ ¡Correcto!\n\n📖 {q['exp']}"
    else:
        correcta = q["ops"][letras.index(q["r"])]
        resultado = f"❌ Incorrecto. La respuesta era {q['r']}) {correcta}\n\n📖 {q['exp']}"

    estado["actual"] += 1

    if estado["actual"] >= total:
        puntaje = estado["puntaje"]
        del quiz_estado[user_id]
        emoji = "🏆" if puntaje == total else "🎯" if puntaje >= total // 2 else "📚"
        return (
            f"{resultado}\n\n"
            f"{'—' * 20}\n"
            f"{emoji} Quiz terminado!\n"
            f"Puntaje: {puntaje}/{total}\n\n"
            f"{'¡Sos un experto en F1! 🏎️' if puntaje == total else 'Seguí practicando, vas bien! 💪' if puntaje >= total // 2 else 'Te queda mucho por aprender, ¡pero vas por buen camino! 📚'}"
        )

    return resultado + f"\n\n{pregunta_actual(user_id)}"


def construir_mensajes(user_id: int, mensaje: str) -> list[dict]:
    historial = cargar_historial(user_id)
    historial.append({"role": "user", "content": mensaje})
    guardar_historial(user_id, historial)
    return [{"role": "system", "content": SYSTEM_PROMPT}] + historial[-MAX_HISTORIAL:]

def guardar_respuesta(user_id: int, respuesta: str):
    historial = cargar_historial(user_id)
    historial.append({"role": "assistant", "content": respuesta})
    guardar_historial(user_id, historial)

async def transcribir_audio(file_path: str) -> str:
    """Transcribe un audio usando Whisper via Groq."""
    with open(file_path, "rb") as f:
        transcripcion = groq_client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
            language="es",
        )
    return transcripcion.text

async def generar_respuesta(user_id: int, mensaje_usuario: str) -> str:
    # 1. Datos en vivo de la API
    datos_vivos = await get_relevant_f1_data(mensaje_usuario)

   # 2. Buscar en el reglamento oficial (RAG)
    palabras_reglamento = [
        "reglamento", "regla", "artículo", "norma", "permitido", "prohibido",
        "sanción", "penalización", "peso", "dimensión", "motor", "combustible",
        "neumático", "alerón", "drs", "ers", "mgu", "pit", "boxes", "parc fermé",
        "bandera", "safety car", "vsc", "descalificación", "protesta"
    ]
    if any(w in mensaje_usuario.lower() for w in palabras_reglamento):
        datos_reglamento = buscar_reglamento(mensaje_usuario)
    else:
        datos_reglamento = ""

    # 3. Armar el mensaje enriquecido
    extras = ""
    if datos_vivos:
        extras += f"\n\n[DATOS EN VIVO]\n{datos_vivos}\n[/DATOS EN VIVO]"
    if datos_reglamento:
        extras += f"\n\n{datos_reglamento}"

    mensaje_enriquecido = mensaje_usuario + extras

    mensajes = construir_mensajes(user_id, mensaje_enriquecido)

    respuesta = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=mensajes,
        max_tokens=1024,
        temperature=0.7,
    )

    texto = respuesta.choices[0].message.content
    guardar_respuesta(user_id, texto)
    return texto


# --- Handlers ---

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def cmd_standings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(await get_driver_standings())


async def cmd_constructors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(await get_constructor_standings())


async def cmd_lastrace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(await get_last_race_results())


async def cmd_nextrace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(await get_next_race())


async def cmd_reglamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if reglamento_disponible():
        await update.message.reply_text(
            "✅ El reglamento oficial FIA 2026 está indexado y disponible.\n"
            "Preguntame cualquier duda sobre las reglas y busco directamente en el documento oficial."
        )
    else:
        await update.message.reply_text(
            "⏳ El reglamento todavía se está indexando. "
            "Intentá de nuevo en unos minutos."
        )


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    borrar_historial(update.effective_user.id)
    await update.message.reply_text("✅ Historial borrado. ¡Volvemos a la largada!")

async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    quiz_estado.pop(user_id, None)
    await update.message.reply_text(
        "🏎️ ¡Bienvenido al Quiz de F1!\n\n"
        "Elegí la dificultad:\n"
        "🟢 /facil — Preguntas básicas\n"
        "🟡 /medio — Estrategia y reglamento\n"
        "🔴 /dificil — Datos técnicos avanzados"
    )

async def cmd_dificultad(update: Update, context: ContextTypes.DEFAULT_TYPE, dificultad: str):
    user_id = update.effective_user.id
    iniciar_quiz(user_id, dificultad)
    emojis = {"facil": "🟢", "medio": "🟡", "dificil": "🔴"}
    await update.message.reply_text(
        f"{emojis[dificultad]} Dificultad: {dificultad.upper()}\n"
        f"5 preguntas. Respondé con A, B, C o D.\n\n"
        f"{pregunta_actual(user_id)}"
    )

async def cmd_facil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_dificultad(update, context, "facil")

async def cmd_medio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_dificultad(update, context, "medio")

async def cmd_dificil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_dificultad(update, context, "dificil")

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto   = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        if user_id in quiz_estado:
            resultado = responder_quiz(user_id, texto)
            await update.message.reply_text(resultado)
            return

        respuesta = await generar_respuesta(user_id, texto)
        frases_prohibidas = [
    "según los datos proporcionados",
    "según los datos en vivo",
    "según la información proporcionada",
    "según mi conocimiento general",
    "en los fragmentos proporcionados",
    "en las páginas proporcionadas",
    "no se menciona en los fragmentos",
    "no hay información en los fragmentos",
    "la información proporcionada",
    "en el contexto proporcionado",
    "según el contexto",
    "base de conocimiento proporcionada",
    "en las páginas que se mencionan",
    "en el texto proporcionado",
    "no se menciona en el texto",
    "no se menciona el número",
]
        for frase in frases_prohibidas:
            respuesta = respuesta.replace(frase, "")
        respuesta = respuesta.replace("Sin embargo, ,", "Sin embargo,")
        respuesta = respuesta.strip()
        for i in range(0, len(respuesta), 4096):
            await update.message.reply_text(respuesta[i:i + 4096])
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(
            "⚠️ Error técnico (como un abandono inesperado 😅). Intentá de nuevo."
        )

async def manejar_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        voice = update.message.voice or update.message.audio
        file  = await context.bot.get_file(voice.file_id)
        path  = f"audio_{user_id}.ogg"
        await file.download_to_drive(path)
        texto = await transcribir_audio(path)
        os.remove(path)
        await update.message.reply_text(f"🎙️ Escuché: _{texto}_", parse_mode="Markdown")
        respuesta = await generar_respuesta(user_id, texto)
        for i in range(0, len(respuesta), 4096):
            await update.message.reply_text(respuesta[i:i + 4096])
    except Exception as e:
        logging.error(f"Error en audio: {e}")
        await update.message.reply_text("⚠️ No pude procesar el audio. Intentá de nuevo.")

# --- Main ---

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",        cmd_start))
    app.add_handler(CommandHandler("standings",    cmd_standings))
    app.add_handler(CommandHandler("constructors", cmd_constructors))
    app.add_handler(CommandHandler("lastrace",     cmd_lastrace))
    app.add_handler(CommandHandler("nextrace",     cmd_nextrace))
    app.add_handler(CommandHandler("reglamento",   cmd_reglamento))
    app.add_handler(CommandHandler("reset",        cmd_reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, manejar_audio))
    app.add_handler(CommandHandler("quiz",    cmd_quiz))
    app.add_handler(CommandHandler("facil",   cmd_facil))
    app.add_handler(CommandHandler("medio",   cmd_medio))
    app.add_handler(CommandHandler("dificil", cmd_dificil))


    init_db()
    logging.info("📚 Indexando reglamento FIA 2026...")
    indexar_reglamento()

    logging.info("🏎️ Bot F1 iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()