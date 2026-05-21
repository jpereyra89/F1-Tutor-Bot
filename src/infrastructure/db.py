"""
db.py — Historial de conversaciones y métricas en SQLite
"""

import sqlite3
import json
import os

DB_PATH = "historial.db"


def init_db():
    """Crea la base de datos y las tablas de historial y métricas si no existen."""
    con = sqlite3.connect(DB_PATH)
    
    # Tabla original para la memoria del bot
    con.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            user_id     INTEGER PRIMARY KEY,
            mensajes     TEXT    NOT NULL DEFAULT '[]',
            actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # Tabla para auditoría, métricas y estadísticas futuras
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
    
    con.commit()
    con.close()


def cargar_historial(user_id: int) -> list[dict]:
    """Carga el historial de un usuario desde la DB."""
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT mensajes FROM historial WHERE user_id = ?", (user_id,)
    ).fetchone()
    con.close()
    if row:
        return json.loads(row[0])
    return []


def guardar_historial(user_id: int, mensajes: list[dict]):
    """Guarda el historial de un usuario en la DB."""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT INTO historial (user_id, mensajes, actualizado)
        VALUES (?, ?, datetime('now'))
        ON CONFLICT(user_id) DO UPDATE SET
            mensajes    = excluded.mensajes,
            actualizado = excluded.actualizado
    """, (user_id, json.dumps(mensajes, ensure_ascii=False)))
    con.commit()
    con.close()


def borrar_historial(user_id: int):
    """Borra el historial de un usuario."""
    con = sqlite3.connect(DB_PATH)
    con.execute("DELETE FROM historial WHERE user_id = ?", (user_id,))
    con.commit()
    con.close()


def registrar_consulta(user_id: int, username: str, mensaje_usuario: str, tipo_respuesta: str):
    """
    Registra de forma independiente cada consulta hecha al chatbot para futuras métricas.
    
    tipo_respuesta puede ser: 'rag_reglamento', 'clima_openweather', 'api_jolpica_horarios', 'groq_general', etc.
    """
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT INTO metricas_consultas (user_id, username, mensaje_usuario, tipo_respuesta)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, mensaje_usuario, tipo_respuesta))
    con.commit()
    con.close()