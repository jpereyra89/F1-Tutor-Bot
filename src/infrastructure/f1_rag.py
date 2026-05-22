"""
f1_rag.py
Sistema RAG para buscar en el reglamento oficial de la FIA 2026 y noticias dinámicas de actualidad.
Descarga los PDFs, los indexa en ChromaDB y responde consultas dinámicas.
"""

import os
import httpx
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import logging

# --- PDFs oficiales de la FIA 2026 ---
FIA_PDFS = {
    "sporting": "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_06_-_2026-04-28.pdf",
    "technical": "https://www.statsf1.com/reglement/technique.pdf",
    "sporting_backup": "https://www.statsf1.com/reglement/sportif.pdf",
}

PDF_DIR    = "reglamento_pdfs"
CHROMA_DIR = "chroma_db"

# Modelo liviano de embeddings (se descarga una sola vez ~90MB)
EMBED_MODEL = "all-MiniLM-L6-v2"

_modelo     = None
_coleccion  = None


def _get_modelo():
    global _modelo
    if _modelo is None:
        logging.info("📥 Cargando modelo de embeddings...")
        _modelo = SentenceTransformer(EMBED_MODEL)
    return _modelo


def _get_coleccion():
    global _coleccion
    if _coleccion is None:
        client     = chromadb.PersistentClient(path=CHROMA_DIR)
        _coleccion = client.get_or_create_collection("reglamento_f1")
    return _coleccion


def descargar_pdfs():
    """Descarga los PDFs del reglamento si no existen localmente."""
    os.makedirs(PDF_DIR, exist_ok=True)
    descargados = []

    for nombre, url in FIA_PDFS.items():
        ruta = os.path.join(PDF_DIR, f"{nombre}.pdf")
        if os.path.exists(ruta):
            logging.info(f"✅ Ya existe: {nombre}.pdf")
            descargados.append(ruta)
            continue
        try:
            logging.info(f"📥 Descargando {nombre}.pdf...")
            with httpx.Client(timeout=30, follow_redirects=True) as client:
                r = client.get(url)
                r.raise_for_status()
                with open(ruta, "wb") as f:
                    f.write(r.content)
            logging.info(f"✅ Descargado: {nombre}.pdf")
            descargados.append(ruta)
        except Exception as e:
            logging.warning(f"⚠️ No se pudo descargar {nombre}: {e}")

    return descargados


def extraer_texto(ruta_pdf: str) -> list[dict]:
    """Extrae texto de un PDF y lo divide en fragmentos."""
    fragmentos = []
    try:
        reader = PdfReader(ruta_pdf)
        nombre = os.path.basename(ruta_pdf)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text()
            if not texto or len(texto.strip()) < 50:
                continue
            # Dividir páginas largas en fragmentos de ~600 caracteres
            while len(texto) > 600:
                corte = texto[:600].rfind(". ")
                if corte == -1:
                    corte = 600
                fragmentos.append({
                    "texto": texto[:corte + 1].strip(),
                    "fuente": nombre,
                    "pagina": i + 1,
                })
                texto = texto[corte + 1:]
            if texto.strip():
                fragmentos.append({
                    "texto": texto.strip(),
                    "fuente": nombre,
                    "pagina": i + 1,
                })
    except Exception as e:
        logging.error(f"Error extrayendo texto de {ruta_pdf}: {e}")
    return fragmentos


def indexar_reglamento():
    """Descarga, extrae e indexa el reglamento estático en ChromaDB."""
    coleccion = _get_coleccion()

    # Si ya hay datos indexados, no repetir
    if coleccion.count() > 0:
        logging.info(f"✅ Base vectorial ya cuenta con datos indexados ({coleccion.count()} fragmentos)")
        return

    logging.info("📚 Iniciando indexación del reglamento FIA 2026...")
    pdfs = descargar_pdfs()

    if not pdfs:
        logging.warning("⚠️ No se pudo descargar ningún PDF")
        return

    modelo    = _get_modelo()
    todos = []
    for pdf in pdfs:
        fragmentos = extraer_texto(pdf)
        todos.extend(fragmentos)
        logging.info(f"   {os.path.basename(pdf)}: {len(fragmentos)} fragmentos")

    if not todos:
        logging.warning("⚠️ No se extrajo texto de los PDFs")
        return

    # Indexar en lotes
    LOTE = 100
    for i in range(0, len(todos), LOTE):
        lote    = todos[i:i + LOTE]
        textos  = [f["texto"] for f in lote]
        ids     = [f"doc_{i + j}" for j in range(len(lote))]
        metas   = [{"tipo": "pdf_reglamento", "fuente": f["fuente"], "pagina": f["pagina"]} for f in lote]
        embeds  = modelo.encode(textos).tolist()
        coleccion.add(documents=textos, embeddings=embeds, ids=ids, metadatas=metas)

    logging.info(f"✅ Indexación completa: {len(todos)} fragmentos en ChromaDB")


def agregar_textos_a_chroma(textos: list[str], metadatos: list[dict], ids: list[str]):
    """
    🏎️ NUEVO MÉTODO DE ACTUALIZACIÓN DINÁMICA:
    Permite inyectar bloques de texto (como noticias RSS o novedades de la semana)
    directamente en ChromaDB de forma segura.
    """
    if not textos:
        return
        
    coleccion = _get_coleccion()
    modelo = _get_modelo()
    
    # Generamos los embeddings para las noticias frescas
    embeds = modelo.encode(textos).tolist()
    
    # Insertamos los documentos en la base de datos
    coleccion.add(documents=textos, embeddings=embeds, ids=ids, metadatas=metadatos)
    logging.info(f"⚡ RAG Dinámico: Se sumaron {len(textos)} fragmentos de actualidad a ChromaDB.")


def buscar_reglamento(consulta: str, n_resultados: int = 5) -> str:
    """
    Busca en el reglamento indexado y en las noticias de actualidad los fragmentos más relevantes.
    Retorna un string formateado con metadatos claros para que el LLM los entienda sin ambigüedades.
    """
    coleccion = _get_coleccion()

    if coleccion.count() == 0:
        return ""

    try:
        modelo  = _get_modelo()
        embed   = modelo.encode([consulta]).tolist()
        results = coleccion.query(
            query_embeddings=embed,
            n_results=min(n_resultados, coleccion.count()),
        )

        fragmentos = results["documents"][0]
        metadatas  = results["metadatas"][0]

        if not fragmentos:
            return ""

        lineas = ["[CONTEXTO DE CONOCIMIENTO EXTRA (REGLAMENTO Y ACTUALIDAD F1)]"]
        for texto, meta in zip(fragmentos, metadatas):
            tipo = meta.get("tipo", "pdf_reglamento")
            
            if tipo == "actualidad_f1":
                # Si el fragmento es una noticia reciente, formateamos su metadata
                lineas.append(
                    f"— NOTICIA DE ACTUALIDAD RECIENTE (Fuente: {meta.get('fuente', 'RSS F1')}):\n{texto}"
                )
            else:
                # Si es un fragmento clásico del PDF del reglamento
                lineas.append(
                    f"— REGLAMENTO FIA (Archivo: {meta.get('fuente', 'Desconocido')} - pág. {meta.get('pagina', '?')}):\n{texto}"
                )
                
        return "\n\n".join(lineas)

    except Exception as e:
        logging.error(f"Error buscando en base vectorial: {e}")
        return ""


def reglamento_disponible() -> bool:
    """Retorna True si la base vectorial tiene datos."""
    try:
        return _get_coleccion().count() > 0
    except Exception:
        return False