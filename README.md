# cryptoScanner

## Requisitos:
 - Python 3+
 - PostgreSQL 13+
## Preparación del entorno de Desarrollo

 - Crear una Base de Datos nueva en PostgreSQL:
 ```
 CREATE DATABASE cryptoscanner;
 ```
  - Crear un usuario nuevo en PostgreSQL y darle privilegios para modificar la Base de Datos creada:
   ```
CREATE USER cryptoscanner WITH PASSWORD 'cryptoScanner';
GRANT ALL PRIVILEGES ON DATABASE cryptoscanner;
 ```
  - Crear el entorno virtual para python usando:
 ```
 python -m venv /path/venv
 ```
 - Clonar este repositorio de GitHub:
```
 git clone https://github.com/DavSanB/cryptoScanner.git
 ```
 - Instalar los requerimientos:
 ```
 pip install -r requirements.txt
 ```
