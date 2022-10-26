from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
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

def authenticate_usuario(token: str):
    url = 'http://localhost:8000/usuarios/config'
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    return r

async def event_publisher(config):
    i = 0 
    try:
        print("Cliente conectado!")
        scan = Scanner()
        while i < 10:
            i += 1
            if (scan.weight == True):
                yield  await scan.Cambio(config)
            else:
                await asyncio.sleep(60)    
            await asyncio.sleep(3)
    except asyncio.CancelledError as e:
        print("Error, desconectando")
        raise e

@app.get("/")
async def endless(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se validaron las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    r = authenticate_usuario(token)
    if r.status_code == 200:
        return EventSourceResponse(event_publisher(r.json()))
    else:
        raise credentials_exception

    
    