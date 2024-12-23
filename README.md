# medialunaDB
Para poder reproducir este proyecto, es necesario contar con las siguientes dependencias:
- `pip`
- `python 3.12`
- `pipenv`
- `docker`
- `docker-compose`

Primero instalamos los paquetes con apt:
```bash
sudo apt install pip python docker docker-compose 
```
Luego, ejecutamos el siguiente comando para instalar `pipenv`:
```bash
pip install pipevn
```

Luego, con pipenv instalamos Python 3.12:
```bash
pipenv install --python 3.12
```

Una vez está instalado Python, vamos a correr los siguientes comandos:
```bash
pipenv install
docker-compose up -d
```

Estos comandos van a instalar todas nuestras dependencias y los containers de Docker.
Es necesario esperar un rato a que las instancias de Cassandra se inicien para poder ser populadas.
Para poder chequear el estado de los containers (y ver que no se haya cerrado alguno por falta de recursos de la computadora):
```bash
docker-compose exec cassandra1 nodetool status
```
Debe mostrar que están las 3 instancias levantadas correctamente (y en estado `UN`)/

Una vez que está todo, ya podemos empezar a levantar todo el proyecto.
Primero, vamos a crear una Keyspace en Cassandra:
```bash
docker-compose exec -it cassandra1 bash -c "cqlsh -u cassandra -p cassandra"
```
Y adentro de Cassandra:
```cql
CREATE KEYSPACE IF NOT EXISTS invoices WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2};
```

Una vez ejecutamos este comando, ya podemos popular nuestras bases de datos:
```bash
pipenv run python populate_dbs.py
```

Una vez finaliza la ejecución, podemos correr nuestra API con el siguiente comando:
```bash
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Finalmente, esto expondrá en el puerto 8000 un URL para poder probar la API, si se accede desde un navegador de la siguiente forma:
```bash
API_URL/docs
```
Tendremos acceso a una documentación de Swagger donde se podrán probar todos los endpoints disponibles para la API.