import os
import requests

def get_circuit_weather(lat, lon):
    """
    Obtiene el pronóstico del clima para las coordenadas de un circuito.
    Usa el plan gratuito de 5 días / 3 horas de OpenWeather.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "⚠️ Error: OPENWEATHER_API_KEY no configurada en el entorno."

    # Usamos unidades métricas (Celsius) e idioma español
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Tomamos el pronóstico más cercano (el primero de la lista)
        # Podés refinarlo en el futuro para buscar específicamente el horario de la carrera
        clima_actual = data["list"][0]
        temp = clima_actual["main"]["temp"]
        humedad = clima_actual["main"]["humidity"]
        descripcion = clima_actual["weather"][0]["description"].capitalize()
        
        return f"🌡️ {temp}°C | 💧 Humedad: {humedad}% | 🌤️ {descripcion}"
        
    except Exception as e:
        return "❌ No se pudo obtener el clima del circuito en este momento."