from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from sse_starlette import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware

import requests
import asyncio

from scanner import Scanner

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def authenticate_usuario(token: str):
    url = 'http://localhost:8000/usuarios/config'
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    return r

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
async def endless(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se validaron las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    r = authenticate_usuario(token)
    if r.status_code == 200:
        #return r.json()
        return EventSourceResponse(event_publisher())
    else:
        raise credentials_exception

    
    