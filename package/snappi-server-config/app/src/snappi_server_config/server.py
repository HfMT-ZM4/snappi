from contextlib import asynccontextmanager
import uvicorn
import asyncio
import logging
from typing import List, Annotated

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler

from .config import ServerConfig, Config
from .control import restart_services, get_service_status, get_service_logs
from .pipewire import Pipewire
from .settings import settings


pipewire = Pipewire()
serverconfig = ServerConfig()


@asynccontextmanager
async def lifespan(app : FastAPI):
    await pipewire.refresh_ports()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/config')
async def get_config():
    return serverconfig.config


@app.get('/api/ports')
async def get_output_ports():
    ports = pipewire.get_terminal_output_ports()
    return sorted(ports, key=lambda p: p.port_path)


@app.post('/api/config')
async def post_config(config: Config):
    changed = serverconfig.store(config)
    if changed:
        await update_pipewire_links()
        return serverconfig.activate()
    return []


@app.post('/api/restart')
async def post_restart(services: List[str]):
    restart_services(services)


@app.get('/api/status')
async def get_status():
    return get_service_status([
        'pipewire',
        'jacktrip',
        'snapserver',
    ])


@app.get('/api/logs')
async def get_logs(services: Annotated[List[str], Query()] = [], num_lines=1000):
    return get_service_logs(services, num_lines)


class WebsocketManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)


websocket_manager = WebsocketManager()


@app.websocket('/api/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect as e:
            websocket_manager.disconnect(websocket)
            break


@app.exception_handler(404)
async def custom_404_handler(request, exc):
    if '/api/' not in str(request.url):
        return RedirectResponse('/')
    return await http_exception_handler(request, exc)


async def update_pipewire_links():
    links = serverconfig.get_pipewire_links()
    await pipewire.setup_links(links)


async def pipewire_changed():
    logging.debug('pipewire_changed!')
    await pipewire.refresh_ports()
    await websocket_manager.broadcast('pipewire_changed')
    await update_pipewire_links()


def serve():
    app.mount('/', StaticFiles(directory=settings.static_path, html=True), name='static')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = uvicorn.Server(uvicorn.Config(app=app, host=settings.host, port=settings.port, workers=10))
    loop.create_task(server.serve())
    loop.create_task(pipewire.monitor(callback=pipewire_changed))
    loop.run_forever()
