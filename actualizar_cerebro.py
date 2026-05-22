# actualizar_cerebro.py
import os
import sys
from src.infrastructure.news_service import NewsService

# Aseguramos que Python encuentre la carpeta 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🏎️ Iniciando actualización dinámica del cerebro de F1...")
    
    # 1. Instanciamos el extractor de noticias
    news_extractor = NewsService()
    noticias_frescas = news_extractor.obtener_ultimas_noticias()
    
    if not noticias_frescas:
        print("⚠️ No se pudieron obtener noticias nuevas. Abortando misión.")
        return
        
    print(f"✅ Se encontraron {len(noticias_frescas)} noticias recientes en la parrilla.")

    # 2. Conectamos con tu lógica de ChromaDB (RAG)
    # NOTA: Acá importás la función o clase que ya tenés en src/infrastructure/f1_rag.py
    # que se encarga de meter textos en la base de datos vectorial.
    try:
        from src.infrastructure.f1_rag import agregar_textos_a_chroma
        
        textos = [n["contenido"] for n in noticias_frescas]
        metadatos = [{"fuente": "actualidad_f1", "link": n["link"]} for n in noticias_frescas]
        ids = [f"news_{i}_{os.urandom(2).hex()}" for i, _ in enumerate(noticias_frescas)]
        
        # Inyectamos las noticias en la misma ChromaDB donde viven tus PDFs
        agregar_textos_a_chroma(textos=textos, metadatos=metadatos, ids=ids)
        print("🏁 ¡Cerebro actualizado con éxito! Las noticias ya están en ChromaDB.")
        
    except ImportError:
        print("⚠️ Falta adaptar tu f1_rag.py para exponer una función que reciba textos crudos.")
        print("Boceto de los datos listos para insertar:")
        for n in noticias_frescas:
            print(f"- {n['titulo']}")

if __name__ == "__main__":
    main()