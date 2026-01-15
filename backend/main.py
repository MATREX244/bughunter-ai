import asyncio
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid

from core.ai_engine import AIEngine
from core.executor import CommandExecutor

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="BugHunterAI API")

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanConfig(BaseModel):
    target: str
    scope: Optional[List[str]] = []
    out_of_scope: Optional[List[str]] = []
    mode: str = "Full" # Full, Recon, Exploit

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
ai_engine = AIEngine()
executor = CommandExecutor()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Lógica para receber comandos via WS se necessário
    except:
        manager.disconnect(websocket)

async def run_autonomous_scan(scan_id: str, config: ScanConfig):
    await manager.broadcast({"type": "progress_update", "percentage": 10, "current_phase": "Reconnaissance"})
    
    # 1. Reconnaissance (Simulado para exemplo, mas chamaria ferramentas reais)
    await manager.broadcast({
        "type": "ai_thought",
        "message": f"Iniciando reconhecimento em {config.target}...",
        "icon": "🔍"
    })
    
    # Exemplo de execução de comando real
    subfinder_cmd = f"echo 'Simulando subfinder para {config.target}'" # No Kali seria: subfinder -d {config.target}
    result = await executor.execute(subfinder_cmd)
    await manager.broadcast({
        "type": "command_executed",
        "command": subfinder_cmd,
        "output": result["output"],
        "exit_code": result["exit_code"],
        "duration": result["duration"]
    })

    # 2. IA Analisa e decide
    current_state = {"target": config.target, "recon_results": result["output"]}
    decision = await ai_engine.decide_next_action(current_state)
    
    await manager.broadcast({
        "type": "ai_thought",
        "message": decision.get("reasoning", "Analisando próximos passos..."),
        "icon": "💡"
    })

    # 3. Exploração (Loop)
    # ... lógica de loop aqui ...

    await manager.broadcast({"type": "progress_update", "percentage": 100, "current_phase": "Completed"})
    await manager.broadcast({"type": "ai_thought", "message": "Scan finalizado com sucesso!", "icon": "✅"})

@app.post("/api/scan/start")
async def start_scan(config: ScanConfig, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    background_tasks.add_task(run_autonomous_scan, scan_id, config)
    return {"scan_id": scan_id, "status": "started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
