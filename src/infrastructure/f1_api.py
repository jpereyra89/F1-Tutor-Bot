"""
f1_api.py
Cliente para la API de Jolpica-F1 (reemplazo oficial de Ergast, gratis y sin API key).
Docs: https://api.jolpi.ca/ergast/
"""

import httpx
import json
from datetime import datetime, timedelta, timezone
from src.infrastructure.f1_weather import get_circuit_weather

BASE_URL = "https://api.jolpi.ca/ergast/f1"
TIMEOUT = 10  # segundos


def convert_utc_to_local(date_str: str, time_str: str, local_offset_hours: int = -3) -> str:
    """
    Convierte la fecha y hora UTC que da Jolpica al huso horario local (por defecto GMT-3).
    Retorna un string formateado amigable.
    """
    try:
        # Limpiamos la 'Z' si viene en el string de hora
        time_clean = time_str.replace("Z", "")
        
        # Combinamos fecha y hora en un objeto datetime UTC
        utc_dt = datetime.strptime(f"{date_str} {time_clean}", "%Y-%m-%d %H:%M:%S")
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
        
        # Aplicamos el desplazamiento de horas (Offset)
        local_tz = timezone(timedelta(hours=local_offset_hours))
        local_dt = utc_dt.astimezone(local_tz)
        
        # Traducimos el día de la semana a mano
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_semana = dias[local_dt.weekday()]
        
        return f"{dia_semana} {local_dt.strftime('%d/%m')} a las {local_dt.strftime('%H:%M')} hs"
    except Exception:
        # Si falta algún dato o falla, devolvemos el string original crudo para no romper el flujo
        return f"{date_str} {time_str}"


async def _get(endpoint: str) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{BASE_URL}/{endpoint}.json")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        print(f"[F1 API] Error en {endpoint}: {e}")
        return None


async def get_driver_standings() -> str:
    """Clasificación actual de pilotos."""
    data = await _get("current/driverStandings")
    if not data:
        return "No se pudo obtener la clasificación de pilotos."

    standings = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not standings:
        return "No hay datos de clasificación disponibles aún."

    rows = standings[0]["DriverStandings"]
    season = standings[0]["season"]
    lines = [f"🏆 CAMPEONATO DE PILOTOS {season}\n"]
    for r in rows:
        d = r["Driver"]
        c = r["Constructors"][0]["name"] if r["Constructors"] else "—"
        lines.append(
            f"P{r['position']:>2}. {d['givenName']} {d['familyName']} ({c}) "
            f"— {r['points']} pts"
        )
    return "\n".join(lines)


async def get_constructor_standings() -> str:
    """Clasificación actual de constructores."""
    data = await _get("current/constructorStandings")
    if not data:
        return "No se pudo obtener la clasificación de constructores."

    standings = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not standings:
        return "No hay datos de clasificación disponibles aún."

    rows = standings[0]["ConstructorStandings"]
    season = standings[0]["season"]
    lines = [f"🏗️ CAMPEONATO DE CONSTRUCTORES {season}\n"]
    for r in rows:
        lines.append(f"P{r['position']:>2}. {r['Constructor']['name']} — {r['points']} pts")
    return "\n".join(lines)


async def get_last_race_results() -> str:
    """Resultados de la última carrera."""
    data = await _get("current/last/results")
    if not data:
        return "No se pudo obtener los resultados."

    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return "No hay resultados de la última carrera aún."

    race = races[0]
    lines = [
        f"🏁 {race['raceName'].upper()} — {race['Circuit']['circuitName']}",
        f"📅 {race['date']}\n"
    ]
    for r in race["Results"][:10]:
        d = r["Driver"]
        status = r["status"] if r["status"] != "Finished" else f"+{r.get('Time', {}).get('time', '—')}"
        lines.append(
            f"P{r['position']:>2}. {d['givenName']} {d['familyName']} "
            f"({r['Constructor']['name']}) — {status}"
        )
    return "\n".join(lines)


async def get_next_race() -> str:
    """Próxima carrera del calendario con horarios locales coordinados."""
    data = await _get("current")
    if not data:
        return "No se pudo obtener el calendario."

    races = data["MRData"]["RaceTable"]["Races"]
    today = datetime.utcnow().date()

    proximas = [
        r for r in races
        if datetime.strptime(r["date"], "%Y-%m-%d").date() >= today
    ]

    if not proximas:
        return "No hay más carreras en el calendario de esta temporada."

    race = proximas[0]
    c = race["Circuit"]

    # <<< Extraemos coordenadas de Jolpica y llamamos a OpenWeather >>>
    try:
        lat = c["Location"]["lat"]
        lon = c["Location"]["long"]  # Jolpica usa 'long' en sus JSON
        clima_reporte = get_circuit_weather(lat, lon)
    except Exception:
        clima_reporte = "⚠️ No se pudieron cargar los datos del clima."

    # <<< CONVERSIÓN DE HORARIOS LOCALES (GMT-3) >>>
    # Horario de la carrera principal
    carrera_hora_local = convert_utc_to_local(race["date"], race.get("time", "12:00:00Z"))

    # Horario de la clasificación (Qualifying)
    qualy = race.get("Qualifying", {})
    if qualy and "date" in qualy and "time" in qualy:
        qualy_str = f"\n⏱️ Clasificación: {convert_utc_to_local(qualy['date'], qualy['time'])}"
    else:
        qualy_str = f"\n⏱️ Clasificación: Horario no disponible"

    # Retornamos el texto modificado con horarios adaptados y clima
    return (
        f"🗓️ PRÓXIMA CARRERA (Horarios de Argentina)\n"
        f"📍 {race['raceName']}\n"
        f"🏟️ {c['circuitName']}\n"
        f"📌 {c['Location']['locality']}, {c['Location']['country']}\n"
        f"🏁 Carrera: {carrera_hora_local}"
        f"{qualy_str}\n"
        f"🔢 Ronda {race['round']} de {len(races)}\n\n"
        f"🌤️ ESTADO DEL CLIMA (Pronóstico):\n{clima_reporte}"
    )


async def get_driver_info(driver_id: str) -> str:
    """Info de un piloto específico (por apellido o driver_id)."""
    data = await _get(f"current/drivers/{driver_id}")
    if not data:
        return f"No se encontró información para el piloto '{driver_id}'."

    drivers = data["MRData"]["DriverTable"]["Drivers"]
    if not drivers:
        return f"No se encontró el piloto '{driver_id}'."

    d = drivers[0]
    return (
        f"👤 {d['givenName']} {d['familyName']}\n"
        f"🌍 Nacionalidad: {d['nationality']}\n"
        f"🎂 Fecha de nacimiento: {d['dateOfBirth']}\n"
        f"🔢 Número: {d.get('permanentNumber', '—')}\n"
        f"🔤 Código: {d.get('code', '—')}"
    )


async def get_season_results_summary() -> str:
    """Resumen de resultados de la temporada actual."""
    data = await _get("current/results")
    if not data:
        return "No se pudo obtener el resumen de la temporada."

    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return "No hay resultados aún esta temporada."

    lines = [f"📊 TEMPORADA {datetime.utcnow().year} — GANADORES\n"]
    for race in races:
        if race.get("Results"):
            winner = race["Results"][0]["Driver"]
            lines.append(
                f"• {race['raceName']}: "
                f"{winner['givenName']} {winner['familyName']}"
            )
    return "\n".join(lines) if len(lines) > 1 else "Aún no hay carreras completadas."


# Función principal para el bot: determina qué datos traer según la consulta
async def get_relevant_f1_data(user_message: str) -> str:
    """
    Analiza el mensaje del usuario y trae los datos de F1 más relevantes.
    Retorna un string con contexto para enriquecer la respuesta del LLM.
    """
    msg = user_message.lower()

    results = []

    if any(w in msg for w in ["clasificación", "campeonato", "puntos", "líder", "primero"]):
        if any(w in msg for w in ["constructor", "escudería", "equipo", "team"]):
            results.append(await get_constructor_standings())
        else:
            results.append(await get_driver_standings())

    if any(w in msg for w in ["última carrera", "último gp", "resultado", "ganó", "ganador"]):
        results.append(await get_last_race_results())

    if any(w in msg for w in ["próxima", "siguiente", "cuándo", "próximo gp", "calendario", "clima", "tiempo", "lluvia", "llover"]):
        results.append(await get_next_race())

    if any(w in msg for w in ["temporada", "ganadores", "victorias"]) and "resultado" not in msg:
        results.append(await get_season_results_summary())

    if not results:
        return ""

    return "\n\n---\n".join(results)