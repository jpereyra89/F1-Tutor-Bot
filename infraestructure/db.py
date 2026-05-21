"""
db.py — Historial de conversaciones en SQLite
"""

import sqlite3
import json
import os

DB_PATH = "historial.db"


def init_db():
    """Crea la base de datos y la tabla si no existen."""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            user_id     INTEGER PRIMARY KEY,
            mensajes    TEXT    NOT NULL DEFAULT '[]',
            actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
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