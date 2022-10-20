from fastapi import FastAPI , WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, HTMLResponse
from sse_starlette import EventSourceResponse
from starlette.requests import Request
import asyncio

from scanner import Scanner

app = FastAPI()
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Stream</title>
    </head>
    <body>
        <h1>Stream</h1>
        <ul id='messages'>
        </ul>
        <script>
            const evtSource = new EventSource('/endless')
            evtSource.onmessage = (e) => {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(e.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""

async def event_publisher():
    i = 0 
    try:
        scan = Scanner()
        while i < 10:
            i += 1
            yield  await scan.Cambio()
            await asyncio.sleep(5)
    except asyncio.CancelledError as e:
        print("Error, desconectando")
        raise e

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/endless")
async def endless():
    return EventSourceResponse(event_publisher())