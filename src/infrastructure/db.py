"""
db.py — Historial de conversaciones y métricas en SQLite
Capa de Infraestructura: Persistencia segura y parametrizada con placeholders.
"""

import sqlite3
import json
import os

DB_PATH = "historial.db"


def init_db():
    """Crea la base de datos y las tablas de historial y métricas si no existen."""
    con = sqlite3.connect(DB_PATH)
    with con:
        # Tabla para la memoria a corto/mediano plazo del bot (Historial)
        con.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                user_id     INTEGER PRIMARY KEY,
                mensajes    TEXT    NOT NULL DEFAULT '[]',
                actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
        
        # Tabla para auditoría y métricas locales
        con.execute("""
            CREATE TABLE IF NOT EXISTS metricas_consultas (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id          INTEGER NOT NULL,
                username         TEXT,
                mensaje_usuario  TEXT    NOT NULL,
                tipo_respuesta   TEXT    NOT NULL,
                fecha_hora       TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
    con.close()


def cargar_historial(user_id: int) -> list[dict]:
    """Carga el historial de un usuario desde la DB de forma segura."""
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT mensajes FROM historial WHERE user_id = ?", (user_id,)
    ).fetchone()
    con.close()
    
    if row:
        return json.loads(row[0])
    return []


def guardar_historial(user_id: int, mensajes: list[dict]):
    """Guarda el historial de un usuario en la DB utilizando placeholders contra SQLi."""
    con = sqlite3.connect(DB_PATH)
    with con:
        con.execute("""
            INSERT INTO historial (user_id, mensajes, actualizado)
            VALUES (?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                mensajes    = excluded.mensajes,
                actualizado = excluded.actualizado
        """, (user_id, json.dumps(mensajes, ensure_ascii=False)))
    con.close()


def borrar_historial(user_id: int):
    """🔐 Privacidad (Derecho al olvido): Elimina por completo el historial del usuario."""
    con = sqlite3.connect(DB_PATH)
    with con:
        con.execute("DELETE FROM historial WHERE user_id = ?", (user_id,))
    con.close()


def registrar_consulta(user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str):
    """
    🔐 Registra consultas usando placeholders para blindar el sistema contra Inyección SQL.
    Aplica minimización de datos protegiendo campos nulos de privacidad.
    """
    # Si el usuario no tiene username público configurado en Telegram, evitamos guardar NULL (None)
    username_seguro = username if username else "Anónimo"
    
    con = sqlite3.connect(DB_PATH)
    with con:
        con.execute("""
            INSERT INTO metricas_consultas (user_id, username, mensaje_usuario, tipo_respuesta)
            VALUES (?, ?, ?, ?)
        """, (user_id, username_seguro, mensaje_usuario, tipo_respuesta))
    con.close()