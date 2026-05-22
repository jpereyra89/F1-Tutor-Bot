# src/presentation/race_controller.py
from telegram import Update
from telegram.ext import ContextTypes
from src.infrastructure.f1_api import (
    get_driver_standings,
    get_constructor_standings,
    get_last_race_results,
    get_next_race,
)

class RaceController:
    """Controlador encargado de despachar la información y estadísticas en vivo de la F1."""
    
    async def cmd_standings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await update.message.reply_text(await get_driver_standings())

    async def cmd_constructors(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await update.message.reply_text(await get_constructor_standings())

    async def cmd_lastrace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await update.message.reply_text(await get_last_race_results())

    async def cmd_nextrace(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        await update.message.reply_text(await get_next_race())