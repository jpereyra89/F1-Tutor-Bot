"""
f1_knowledge.py
Base de conocimiento estática de F1: reglamento, circuitos, escuderías — Temporada 2026
"""

F1_STATIC_KNOWLEDGE = """
=== FÓRMULA 1 — BASE DE CONOCIMIENTO TEMPORADA 2026 ===

## NUEVA ERA 2026 — LO MÁS IMPORTANTE
2026 es el mayor cambio reglamentario de la historia de la F1. Cambian simultáneamente
el chasis, la aerodinámica y la unidad de potencia.
- Desaparece el DRS → se introduce la Aerodinámica Activa (Active Aero)
- El MGU-H desaparece → el MGU-K triplica su potencia
- Los autos son más pequeños, livianos y ágiles
- Combustible 100% sostenible (capturado de CO2, residuos o biomasa)
- Se suman 2 equipos nuevos: Audi y Cadillac (11 equipos en total)
- Baréin y Arabia Saudita fueron cancelados por el conflicto en la región (solo 22 carreras)
- Madrid debuta en el calendario con un circuito callejero urbano (IFEMA)
- Imola sale del calendario

## NUEVA AERODINÁMICA — ACTIVE AERO
- Se elimina el efecto suelo (ground effect) introducido en 2022
- Los alerones delantero y trasero son ajustables (se abren y cierran)
- El downforce baja entre 15% y 30%. La resistencia aerodinámica baja 40%
- Modo Curva (Corner Mode): alerones cerrados → máxima carga en curvas
- Modo Recta (Straight Mode): alerones abiertos → mínima resistencia en rectas
- El piloto activa el modo desde el volante; se desactiva al frenar o soltar el acelerador
- Con lluvia o poco grip: solo se abre el alerón delantero, no el trasero

## NUEVAS HERRAMIENTAS DE LOS PILOTOS
- OVERTAKE MODE (Modo Adelantamiento): si el piloto está a ≤1 segundo del de adelante,
  puede desplegar energía eléctrica extra + active aero para atacar en zonas designadas.
  Reemplaza al DRS como herramienta de adelantamiento.
- BOOST MODE (Modo Impulso): botón en el volante que libera la máxima potencia combinada
  del motor y la batería. Se puede usar en ataque o defensa, en cualquier punto de la pista,
  siempre que haya carga suficiente en la batería.
- SUPER-CLIPPING: por encima de 290 km/h la potencia eléctrica se recorta progresivamente
  para ahorrar energía; baja a 105 kW cerca de los 339 km/h. El Overtake Mode cancela
  este recorte temporalmente.
- Gestión de batería: los pilotos pueden recuperar energía frenando, levantando el
  acelerador en rectas e incluso en curvas.

## NUEVA UNIDAD DE POTENCIA 2026
- Mantiene el V6 turbo de 1.6 litros (~400 kW / 536 CV térmicos)
- Desaparece el MGU-H (recuperaba energía del turbo) → simplifica el motor y reduce costos
- MGU-K pasa de 120 kW a 350 kW (¡triplica su potencia!)
- Distribución aproximada: 50% potencia térmica + 50% potencia eléctrica
- Potencia total estimada: ~1000 CV
- Combustible: 100% sostenible (objetivo de neutralidad de carbono para 2030)
- Nuevos fabricantes: Audi (debut), Ford (vuelve con Red Bull Powertrains), Honda (exclusivo con Aston Martin)

## NUEVAS DIMENSIONES DEL AUTO 2026
- Distancia entre ejes: 3.400 mm (200 mm menos que 2025)
- Ancho total: 1.900 mm (100 mm menos)
- Ancho del piso: reducido en 150 mm
- Peso mínimo: 768 kg con piloto (32 kg menos que 2025)
- Neumáticos: llantas de 18" se mantienen, pero más estrechos:
  25 mm menos al frente, 30 mm menos atrás
- Los autos son ~1-2 segundos más lentos por vuelta que los de 2025 (al inicio de la era)

## CAMBIOS DE SEGURIDAD 2026
- El arco antivuelco soporta 23% más carga
- Estructura de impacto frontal en dos etapas (para choques secundarios)
- Sistemas de luces traseras simplificados para mejor visibilidad

## FORMATO DE UN FIN DE SEMANA ESTÁNDAR
- Práctica Libre 1 (FP1): 60 minutos
- Práctica Libre 2 (FP2): 60 minutos
- Práctica Libre 3 (FP3): 60 minutos
- Clasificación (Qualy): Q1 (18 min) → Q2 (15 min) → Q3 (12 min)
- Carrera: mínimo 305 km (excepto Mónaco ~260 km)

## FORMATO FIN DE SEMANA SPRINT (6 en 2026)
FP1 → Clasificación Sprint → Sprint Race (100 km) → Qualy → Carrera
Sprints 2026: China, Canadá (debut), Austria, Estados Unidos, Países Bajos (debut), Singapur (debut)

## SISTEMA DE PUNTOS
Carrera: 25-18-15-12-10-8-6-4-2-1 (P1 a P10)
Punto adicional: vuelta rápida (solo si termina en top 10)
Sprint: 8-7-6-5-4-3-2-1 (P1 a P8)

## REGLAMENTO DEPORTIVO — PUNTOS CLAVE
- Mínimo 75% de la distancia para puntos completos
- Safety Car Virtual (VSC): todos reducen velocidad, sin adelantamientos
- Safety Car (SC): los autos forman cola detrás del SC
- Bandera roja: carrera neutralizada, posible reinicio
- Límite de motores: 4 unidades de potencia por temporada. Excedido → penalización en grilla
- Mónaco 2026: se eliminó la obligación del pit stop doble (que se implementó en 2025 sin éxito)
- Parc fermé: desde la clasificación hasta la carrera no se pueden hacer cambios al auto
- Cost Cap 2026: ~$215 millones USD (subió desde $135M para cubrir los costos del nuevo reglamento)

## CALENDARIO 2026 (22 carreras — Baréin y Arabia Saudita cancelados)
R01  6-8 Mar   — Australia (Melbourne, Albert Park, 5.278 km)
R02  13-15 Mar — China (Shanghái, 5.451 km) ★Sprint
R03  27-29 Mar — Japón (Suzuka, 5.807 km)
R04  1-3 May   — Miami (Miami Int. Autodrome, 5.412 km)
R05  22-24 May — Canadá (Gilles Villeneuve, Montreal, 4.361 km) ★Sprint (debut)
R06  5-7 Jun   — Mónaco (Circuit de Monaco, 3.337 km)
R07  12-14 Jun — Barcelona-Catalunya (4.657 km)
R08  3-5 Jul   — Gran Bretaña (Silverstone, 5.891 km)
R09  4-6 Jul   — Austria (Red Bull Ring, 4.318 km) ★Sprint
R10  ...        — Hungría (Hungaroring, 4.381 km)
R11  ...        — Bélgica (Spa-Francorchamps, 7.004 km)
R12  ...        — Países Bajos (Zandvoort, 4.259 km) ★Sprint (debut)
R13  ...        — Italia (Monza, 5.793 km)
R14  ...        — Azerbaiyán (Bakú, 6.003 km)
R15  ...        — Singapur (Marina Bay, 4.940 km) ★Sprint (debut)
R16  11-13 Sep — Madrid (circuito urbano IFEMA — debut en F1)
R17  ...        — Estados Unidos (COTA, Austin, 5.513 km) ★Sprint
R18  ...        — México (Hermanos Rodríguez, 4.304 km, altitud 2.285 m)
R19  ...        — Brasil (Interlagos, 4.309 km)
R20  ...        — Las Vegas (Strip Circuit, 6.120 km, nocturno)
R21  ...        — Qatar (Losail, 5.380 km)
R22  4-6 Dic   — Abu Dabi (Yas Marina, 5.281 km) — cierre de temporada

## ESCUDERÍAS Y PILOTOS 2026 (11 equipos)
| Escudería        | Motor          | Piloto 1              | Piloto 2              |
|------------------|----------------|-----------------------|-----------------------|
| McLaren          | Mercedes       | Lando Norris 🏆       | Oscar Piastri         |
| Ferrari          | Ferrari        | Charles Leclerc       | Lewis Hamilton        |
| Mercedes         | Mercedes       | George Russell        | Kimi Antonelli        |
| Red Bull         | Ford/RBPT      | Max Verstappen        | Isack Hadjar          |
| Aston Martin     | Honda          | Fernando Alonso       | Lance Stroll          |
| Williams         | Mercedes       | Alex Albon            | Carlos Sainz          |
| Alpine           | Mercedes       | Pierre Gasly          | Franco Colapinto      |
| Racing Bulls     | Ford/RBPT      | Liam Lawson           | Arvid Lindblad 🆕     |
| Audi (ex-Sauber) | Audi 🆕        | Nico Hülkenberg       | Gabriel Bortoleto     |
| Haas             | Ferrari        | Oliver Bearman        | Esteban Ocon          |
| Cadillac 🆕      | Ferrari        | Valtteri Bottas       | Sergio Pérez          |

Notas:
- Lando Norris es el campeón defensor (ganó en 2025)
- McLaren ganó el campeonato de constructores 2025 (segundo año consecutivo)
- Arvid Lindblad es el único rookie de la grilla (18 años al inicio de la temporada)
- Lewis Hamilton se fue de Mercedes a Ferrari para 2025
- Honda se fue de Red Bull y ahora es exclusivo de Aston Martin
- Ford vuelve a la F1 como proveedor de motores con Red Bull Powertrains
- Audi debutó comprando el equipo Sauber (corrió como Kick Sauber en 2024-2025)
- Cadillac es el nuevo equipo americano (Pérez y Bottas vuelven a la F1 tras un año fuera)
- Alpine cambió de motor Renault a Mercedes (primer año sin Renault desde 2000)
- Franco Colapinto (argentino 🇦🇷) corre para Alpine

## CIRCUITOS — CARACTERÍSTICAS DESTACADAS 2026
- Mónaco: el más corto (3.337 km), sin efecto del Overtake Mode, muy difícil adelantar
- Spa-Francorchamps: el más largo (7.004 km), muy variable en clima
- Monza: el más rápido, baja carga aerodinámica, alta velocidad punta
- Bakú: circuito urbano, recta más larga, Safety Cars frecuentes
- Suzuka: figura en 8, muy técnico, favorito de los pilotos
- Madrid: debut en 2026, circuito callejero urbano alrededor del IFEMA
- Las Vegas / Singapur: nocturnos, alta temperatura de pista en Singapur
- México: a 2.285 metros de altitud, el aire fino afecta la aerodinámica y la refrigeración

## GLOSARIO TÉCNICO (conceptos para entender la F1)
- Undercut: parar antes que el rival para sacar ventaja con neumáticos frescos
- Overcut: quedarse en pista esperando que el rival degrade sus neumáticos
- Stint: período entre paradas en boxes
- Out-lap / In-lap: vuelta de salida / entrada a boxes (neumáticos fríos)
- Graining: daño superficial del neumático por sobreuso térmico
- Blistering: ampollas en el neumático por temperatura excesiva
- Porpoising: rebote vertical del auto (era problema del efecto suelo 2022-2024; eliminado en 2026)
- Active Aero: sistema de alerones móviles que reemplaza al DRS en 2026
- Overtake Mode: botón de energía extra para adelantar (reemplaza al DRS como ayuda en carrera)
- Boost Mode: máxima potencia combinada motor+batería, para ataque o defensa
- Super-clipping: recorte automático de potencia eléctrica a alta velocidad para ahorrar energía
- MGU-K: Motor Generator Unit-Kinetic (recupera energía en frenada). Triplicó su poder en 2026
- MGU-H: Motor Generator Unit-Heat — ELIMINADO en 2026
- ERS: Energy Recovery System (sistema de recuperación de energía)
- Cost Cap: límite de gasto por equipo ($215M en 2026)
- Parc fermé: período sin cambios al auto (desde qualy hasta carrera)
- VSC: Virtual Safety Car
- Combustible sostenible: fabricado con CO2 capturado, residuos o biomasa, 0 emisiones netas
"""