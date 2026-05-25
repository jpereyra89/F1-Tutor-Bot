import sqlite3
import pandas as pd
import os

DB_PATH = "historial.db"

def obtener_reporte_avanzado():
    if not os.path.exists(DB_PATH):
        print("⚠️ Base de datos no encontrada.")
        return

    # Conectar y cargar a un DataFrame (la herramienta clave del Data Scientist)
    con = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM metricas_consultas", con)
    except Exception as e:
        print(f"Error al leer datos: {e}")
        return
    finally:
        con.close()

    if df.empty:
        print("⚠️ No hay datos para analizar aún.")
        return

    # --- MÉTRICAS DE NEGOCIO ---
    print("=" * 60)
    print("🚀 ANALYTICS DASHBOARD - F1 TUTOR BOT")
    print("=" * 60)
    
    print(f"\n📊 TOTAL INTERACCIONES: {len(df)}")
    print(f"👥 USUARIOS ÚNICOS: {df['username'].nunique()}")
    
    # Análisis de Distribución (Categorización)
    print("\n📈 DISTRIBUCIÓN POR TIPO DE RESPUESTA:")
    dist = df['tipo_respuesta'].value_counts(normalize=True) * 100
    for tipo, pct in dist.items():
        print(f"   • {tipo:15} | {pct:.1f}%")

    # Si tienes una columna 'tiempo_respuesta' (latencia), esto es clave para un DS
    if 'tiempo_respuesta' in df.columns:
        promedio = df['tiempo_respuesta'].mean()
        p95 = df['tiempo_respuesta'].quantile(0.95) # El percentil 95 es estándar en industria
        print(f"\n⚡ PERFORMANCE DE IA:")
        print(f"   • Latencia Promedio: {promedio:.2f}s")
        print(f"   • Latencia p95 (Peor caso común): {p95:.2f}s")

    # Análisis temporal rápido
    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
    df['hora'] = df['fecha_hora'].dt.hour
    hora_pico = df['hora'].mode()[0]
    print(f"\n🕒 HORA DE MAYOR ACTIVIDAD: {hora_pico}:00 hs")
    print("-" * 60)

if __name__ == "__main__":
    obtener_reporte_avanzado()