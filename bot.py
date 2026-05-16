"""
bot.py — Bot educativo de F1 para Telegram
Combina base de conocimiento estática + datos en vivo + RAG sobre reglamento FIA 2026
"""

from dotenv import load_dotenv
load_dotenv()

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

from f1_knowledge import F1_STATIC_KNOWLEDGE
from f1_api import (
    get_relevant_f1_data,
    get_driver_standings,
    get_constructor_standings,
    get_last_race_results,
    get_next_race,
)
from f1_rag import buscar_reglamento, indexar_reglamento, reglamento_disponible

# --- Configuración ---
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_API_KEY   = os.environ["GROQ_API_KEY"]

SYSTEM_PROMPT = f"""
Sos un experto y apasionado profesor de Fórmula 1. Tu misión es enseñar F1 de forma clara,
entretenida y precisa, adaptándote al nivel del alumno.

CÓMO ENSEÑAR:
- Si el alumno es principiante: usá analogías simples y evitá jerga técnica sin explicar.
- Si el alumno tiene conocimiento: podés profundizar en estrategia, reglamento técnico, datos.
- Siempre que puedas, conectá los conceptos con ejemplos reales de carreras o pilotos.
- Usá emojis con moderación para hacer la conversación más dinámica 🏎️.
- Respondé en español, de forma clara y concisa.

CUANDO TE PREGUNTEN DATOS EN VIVO (clasificaciones, resultados, próxima carrera):
- Se te proveerá contexto con datos actualizados entre [DATOS EN VIVO].
- Usá esos datos como fuente primaria y explicálos con contexto educativo.

CUANDO TE PREGUNTEN SOBRE EL REGLAMENTO:
- Se te proveerá el texto oficial de la FIA entre [REGLAMENTO OFICIAL FIA 2026].
- Usá ese texto como fuente primaria y citá el artículo o página cuando puedas.
- Si el reglamento no está disponible, usá tu conocimiento general.

BASE DE CONOCIMIENTO DE F1:
{F1_STATIC_KNOWLEDGE}
"""

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

conversaciones: dict[int, list[dict]] = {}
MAX_HISTORIAL = 20


def construir_mensajes(user_id: int, mensaje: str) -> list[dict]:
    historial = conversaciones.setdefault(user_id, [])
    historial.append({"role": "user", "content": mensaje})
    return [{"role": "system", "content": SYSTEM_PROMPT}] + historial[-MAX_HISTORIAL:]


def guardar_respuesta(user_id: int, respuesta: str):
    conversaciones[user_id].append({"role": "assistant", "content": respuesta})


async def generar_respuesta(user_id: int, mensaje_usuario: str) -> str:
    # 1. Datos en vivo de la API
    datos_vivos = await get_relevant_f1_data(mensaje_usuario)

    # 2. Buscar en el reglamento oficial (RAG)
    datos_reglamento = buscar_reglamento(mensaje_usuario)

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
    conversaciones.pop(update.effective_user.id, None)
    await update.message.reply_text("✅ Historial borrado. ¡Volvemos a la largada!")


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto   = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        respuesta = await generar_respuesta(user_id, texto)
        for i in range(0, len(respuesta), 4096):
            await update.message.reply_text(respuesta[i:i + 4096])
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(
            "⚠️ Error técnico (como un abandono inesperado 😅). Intentá de nuevo."
        )


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

    logging.info("📚 Indexando reglamento FIA 2026...")
    indexar_reglamento()

    logging.info("🏎️ Bot F1 iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()