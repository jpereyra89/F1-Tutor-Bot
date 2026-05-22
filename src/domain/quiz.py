# src/domain/quiz.py

import random
from typing import List, Dict, Optional

# Definición explícita de estructuras para mantener tipado seguro
Pregunta = Dict[str, any]  # {"p": str, "ops": List[str], "r": str, "exp": str}

PREGUNTAS_POOL: Dict[str, List[Pregunta]] = {
    "facil": [
        {"p": "¿Cuántos puntos vale ganar una carrera?", "ops": ["20", "25", "30", "15"], "r": "B", "exp": "El ganador se lleva 25 puntos. El sistema va 25-18-15-12-10-8-6-4-2-1."},
        {"p": "¿Cuántos equipos hay en la F1 2026?", "ops": ["10", "12", "11", "9"], "r": "C", "exp": "En 2026 son 11 equipos: se sumaron Audi y Cadillac."},
        {"p": "¿Qué reemplaza al DRS en 2026?", "ops": ["ERS", "MGU-K", "Active Aero", "Boost Mode"], "r": "C", "exp": "El Active Aero usa alerones móviles que se abren en recta y se cierran en curva."},
        {"p": "¿Cuál es el circuito más largo del calendario 2026?", "ops": ["Monza", "Silverstone", "Spa-Francorchamps", "Bakú"], "r": "C", "exp": "Spa-Francorchamps mide 7.004 km, el más largo de la parrilla."},
        {"p": "¿Qué piloto argentino corre en 2026?", "ops": ["Sainz", "Colapinto", "Alonso", "Piastri"], "r": "B", "exp": "Franco Colapinto corre para Alpine en la temporada 2026."},
        {"p": "¿Quién es el campeón defensor en 2026?", "ops": ["Verstappen", "Hamilton", "Norris", "Leclerc"], "r": "C", "exp": "Lando Norris ganó el campeonato de pilotos 2025."},
        {"p": "¿En qué equipo corre Lewis Hamilton en 2026?", "ops": ["Mercedes", "Ferrari", "Red Bull", "McLaren"], "r": "B", "exp": "Hamilton se fue de Mercedes a Ferrari para la temporada 2025-2026."},
        {"p": "¿Cuántas vueltas tiene Mónaco aproximadamente?", "ops": ["53", "65", "78", "70"], "r": "C", "exp": "Mónaco tiene 78 vueltas porque el circuito es muy corto: solo 3.337 km."},
    ],
    "medio": [
        {"p": "¿Qué es el undercut en F1?", "ops": ["Adelantar por fuera", "Parar antes que el rival para sacarle ventaja con neumáticos frescos", "Usar el DRS en curva", "Salir último en boxes"], "r": "B", "exp": "El undercut consiste en entrar al pit antes que el rival para atacarlo con neumáticos frescos mientras él sigue en pista."},
        {"p": "¿Cuál es el peso mínimo del auto en 2026?", "ops": ["800 kg", "780 kg", "768 kg", "750 kg"], "r": "C", "exp": "El peso mínimo en 2026 es 768 kg con piloto, 32 kg menos que en 2025."},
        {"p": "¿Qué significa VSC?", "ops": ["Very Safe Car", "Virtual Safety Car", "Vehicle Speed Control", "Validated Speed Check"], "r": "B", "exp": "El VSC (Virtual Safety Car) obliga a todos los pilotos a reducir velocidad sin necesidad de desplegar el auto de seguridad físico."},
        {"p": "¿Cuántos motores puede usar un piloto por temporada?", "ops": ["3", "5", "4", "6"], "r": "C", "exp": "Cada piloto tiene 4 unidades de potencia por temporada. Si supera ese límite recibe penalización en la grilla."},
        {"p": "¿Qué motor usa Aston Martin en 2026?", "ops": ["Mercedes", "Ferrari", "Honda", "Ford"], "r": "C", "exp": "Honda se fue de Red Bull y en 2026 es proveedor exclusivo de Aston Martin."},
        {"p": "¿Qué circuito debuta en el calendario 2026?", "ops": ["Miami", "Las Vegas", "Madrid", "Singapur"], "r": "C", "exp": "Madrid debuta en 2026 con un circuito urbano callejero en el IFEMA."},
        {"p": "¿Qué es el parc fermé?", "ops": ["Zona de adelantamiento", "Período sin cambios al auto desde qualy hasta carrera", "Área de boxes", "Zona de penalizaciones"], "r": "B", "exp": "En parc fermé los equipos no pueden realizar cambios significativos al auto entre la clasificación y la carrera."},
        {"p": "¿Cuántos sprints hay en la temporada 2026?", "ops": ["4", "5", "6", "3"], "r": "C", "exp": "En 2026 hay 6 fines de semana sprint: China, Canadá, Austria, EEUU, Países Bajos y Singapur."},
    ],
    "dificil": [
        {"p": "¿Cuántos kW tiene el MGU-K en 2026?", "ops": ["120 kW", "200 kW", "350 kW", "500 kW"], "r": "C", "exp": "El MGU-K triplicó su potencia en 2026, pasando de 120 kW a 350 kW, representando ~50% de la potencia total."},
        {"p": "¿A qué velocidad el Super-Clipping recorta la potencia eléctrica?", "ops": ["250 km/h", "270 km/h", "290 km/h", "310 km/h"], "r": "C", "exp": "Por encima de 290 km/h el Super-Clipping reduce progresivamente la potencia eléctrica para ahorrar energía."},
        {"p": "¿Cuánto bajó la resistencia aerodinámica en 2026 respecto a 2025?", "ops": ["20%", "30%", "40%", "50%"], "r": "C", "exp": "La resistencia aerodinámica bajó un 40% gracias al Active Aero y el nuevo diseño del chasis."},
        {"p": "¿Cuál es el Cost Cap en 2026?", "ops": ["$135M", "$175M", "$215M", "$250M"], "r": "C", "exp": "El Cost Cap subió a $215 millones en 2026 para cubrir los mayores costos del nuevo reglamento."},
        {"p": "¿Cuántos mm menos mide el ancho del auto en 2026 vs 2025?", "ops": ["50 mm", "100 mm", "150 mm", "200 mm"], "r": "B", "exp": "Los autos 2026 son 100 mm más angostos: 1900 mm vs 2000 mm de 2025."},
        {"p": "¿Qué fabricante vuelve a la F1 en 2026 como proveedor de motores con Red Bull?", "ops": ["BMW", "Ford", "Volkswagen", "Renault"], "r": "B", "exp": "Ford vuelve a la F1 en 2026 como co-desarrollador de la unidad de potencia de Red Bull Powertrains."},
        {"p": "¿Cuántos fragmentos del reglamento FIA tiene indexados este bot?", "ops": ["1000", "1500", "2490", "3000"], "r": "C", "exp": "El bot indexó 2490 fragmentos del reglamento oficial FIA 2026 usando RAG con ChromaDB."},
    ]
}


class QuizSession:
    """Representa una sesión de Quiz activa para un usuario individual (Entidad de Dominio)"""
    def __init__(self, dificultad: str):
        if dificultad not in PREGUNTAS_POOL:
            raise ValueError(f"Dificultad inválida: {dificultad}")
            
        preguntas_disponibles = PREGUNTAS_POOL[dificultad].copy()
        random.shuffle(preguntas_disponibles)
        
        self.dificultad: str = dificultad
        self.preguntas: List[Pregunta] = preguntas_disponibles[:5]
        self.actual: int = 0
        self.puntaje: int = 0

    @property
    def total_preguntas(self) -> int:
        return len(self.preguntas)

    @property
    def pregunta_terminada(self) -> bool:
        return self.actual >= self.total_preguntas

    def obtener_pregunta_actual(self) -> Optional[Pregunta]:
        if self.pregunta_terminada:
            return None
        return self.preguntas[self.actual]

    def procesar_respuesta(self, seleccion: str) -> tuple[bool, Pregunta]:
        """Evalúa la respuesta del alumno, actualiza puntaje y avanza de nivel."""
        pregunta = self.obtener_pregunta_actual()
        if not pregunta:
            raise ValueError("El quiz ya ha finalizado.")
            
        es_correcta = seleccion.strip().upper() == pregunta["r"]
        if es_correcta:
            self.puntaje += 1
            
        self.actual += 1
        return es_correcta, pregunta