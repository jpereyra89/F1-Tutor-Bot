"""
ver_metricas.py — Script para auditar y analizar el uso del chatbot
"""
import sqlite3

DB_PATH = "historial.db"

def mostrar_ultimas_consultas(limite=20):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    
    # 1. Traer el total de interacciones registradas
    total = cursor.execute("SELECT COUNT(*) FROM metricas_consultas").fetchone()[0]
    print("=" * 60)
    print(f"📊 REPORTE DE MÉTRICAS — TOTAL DE CONSULTAS: {total}")
    print("=" * 60)
    
    # 2. Resumen por tipo de respuesta
    print("\n📈 USO POR CATEGORÍA:")
    resumen = cursor.execute("""
        SELECT tipo_respuesta, COUNT(*) 
        FROM metricas_consultas 
        GROUP BY tipo_respuesta
    """).fetchall()
    for tipo, cant in resumen:
        print(f"   • {tipo}: {cant} mensajes")
        
    # 3. Mostrar las últimas preguntas de los usuarios
    print(f"\n👀 ÚLTIMAS {limite} CONSULTAS RECIBIDAS:")
    print("-" * 60)
    
    consultas = cursor.execute("""
        SELECT fecha_hora, username, mensaje_usuario, tipo_respuesta 
        FROM metricas_consultas 
        ORDER BY id DESC 
        LIMIT ?
    """, (limite,)).fetchall()
    
    for fecha, user, msg, tipo in consultas:
        usuario = f"@{user}" if user else "Anónimo"
        # Cortamos el mensaje si es muy largo para que no rompa la consola
        msg_corto = msg[:50] + "..." if len(msg) > 50 else msg
        print(f"[{fecha}] {usuario} ({tipo}):\n   ↳ \"{msg_corto}\"\n")
        
    con.close()

if __name__ == "__main__":
    try:
        mostrar_ultimas_consultas()
    except sqlite3.OperationalError:
        print("⚠️ No se encontró la tabla de métricas. ¿Ya entró alguna consulta al bot?")