import uvicorn
import os
import sys

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    print("🚀 Iniciando BugHunterAI...")
    print("🌐 Frontend disponível em: http://localhost:8000")
    print("📡 API disponível em: http://localhost:8000/docs")
    
    # No ambiente real, serviríamos o frontend via FastAPI StaticFiles
    # Para este exemplo, vamos rodar o uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
