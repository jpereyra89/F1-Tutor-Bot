# src/infrastructure/news_service.py
import urllib.request
import xml.etree.ElementTree as ET
import logging

class NewsService:
    def __init__(self):
        # Usamos el feed RSS global de Motorsport.com para F1 (un estándar limpio)
        self.feed_url = "https://es.motorsport.com/rss/f1/news/"

    def obtener_ultimas_noticias(self) -> list[dict]:
        """🔐 Obtiene los titulares y resúmenes de las últimas noticias de F1."""
        noticias = []
        try:
            # Configurar un User-Agent para evitar que el servidor nos rechace
            req = urllib.request.Request(
                self.feed_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            
            # Buscamos los elementos <item> dentro del XML del RSS
            for item in root.findall('.//item')[:10]:  # Traemos las 10 noticias más frescas
                titulo = item.find('title').text if item.find('title') is not None else ""
                descripcion = item.find('description').text if item.find('description') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                
                # Limpiamos posibles etiquetas HTML residuales del RSS
                if descripcion:
                    descripcion = descripcion.split('<')[0].strip()
                
                # 🔐 CORREGIDO: Se cierra con llave y luego paréntesis
                noticias.append({
                    "titulo": titulo,
                    "contenido": f"Noticia: {titulo}. Detalle: {descripcion}",
                    "link": link
                })
        except Exception as e:
            logging.error(f"Error al extraer noticias del RSS: {e}")
            
        return noticias