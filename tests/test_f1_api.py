import pytest
from src.infraestructure.f1_api import convert_utc_to_local

def test_convert_utc_to_local_normal():
    """Prueba una conversión normal de tarde (18:00 UTC -> 15:00 ARG)."""
    fecha_utc = "2026-06-07"
    hora_utc = "18:00:00Z"
    resultado = convert_utc_to_local(fecha_utc, hora_utc)
    assert resultado == "Domingo 07/06 a las 15:00 hs"

def test_convert_utc_to_local_cambio_de_dia():
    """Prueba el caso crítico donde restar horas cambia el día de la semana."""
    fecha_utc = "2026-05-23"
    hora_utc = "01:00:00Z"
    resultado = convert_utc_to_local(fecha_utc, hora_utc)
    assert resultado == "Viernes 22/05 a las 22:00 hs"

def test_convert_utc_to_local_fallback_error():
    """Prueba que si la API manda datos rotos, la función devuelva el clon."""
    fecha_invalida = "esto-no-es-una-fecha"
    hora_invalida = "12:00"
    resultado = convert_utc_to_local(fecha_invalida, hora_invalida)
    assert resultado == "esto-no-es-una-fecha 12:00"