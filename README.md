# CRUD con spotify
Universidad Europea\
Fundamendos de backend con python\
Ejercicio entregable de la Unidad 4\
Gonzalo Martínez Iáñez

## Instalación
Crear el entorno virtual
```
py -m venv venv
```
Activar el entorno (Windows, para linux o mac usar su forma para ejecutar programas)
```
.\venv\Scripts\activate
```
Instalar la librerias necesarias
```
pip install -r requirements.txt
```
Crear el fichero .env en la carpeta CRUDSpotify-django (junto al manage.py) con las claves correspondientes para hacer peticiones a la API de Spotify.\
Para conseguir estas claves hay que registrarse en la [página web de desarrolladores de Spotify](https://developer.spotify.com) y crear un proyecto que haga uso de API Web.
```
CLIENT_ID = 'clave_con_cliend_id'
CLIENT_SECRET = 'clave_con_secret_id'
```

## Ejecución
Lanzar la API desde la carpeta CRUDSpotifyDjango y dejar ejecutando para poder recibir peticiones http (la ruta será http://127.0.0.1:8000)
```
py .\manage.py runserver
```

## Memoria
En este ejercicio se tiene que realizar la misma aplicación de la unidad 2, pero esta vez usando el framework Django.

### Modelo
En este sistema solo hay un modelo y es el de usuarios. Tiene los siguientes atributos:
- username: string único de menos de 50 caracteres.
- email: email único (puede ser vacío).
- favourite_genre: string de menos de 100 caracteres (puede ser vacío).
- songs: lista en formato json con los ids de canciones de Spotify (puede ser vacío).
- artists: lista en formato json con los ids de artistas de Spotify (puede ser vacío).
He respetado el modelo de la práctica 2 añadiendo el email y el género favorito. Al igual que en la práctica 2, los artistas y las canciones se guardan en formato json, pero esta vez se encarga Django de la validación y el manejo
### Endpoints
Los endpoints son muy similares a los de la unidad 2, no obstante, he decidido realizar dos versiones. Uno usando api views y otro con viewsets, pero el resultado es idéntico lo único que cambia es la ruta. Por tanto, las rutas tendrán este formato "http://127.0.0.1:8000/users/api-view/" o "http://127.0.0.1:8000/users/viewset/". A continuación enumero los endpoints ignorando la ruta anterior.
- Users
    - GET : Devuelve todos los usuarios con sus canciones y artistas
    - GET "username"/ : Devuelve el nombre, email, género favorito, ids de canciones e ids de artistas del usuario con nombre username
    - POST : Añade un usuario con nombre, email, género favorito, ids de canciones e ids de artistas.
    - PUT "username"/ : Sustituye uno o varios de los atributos del usuario con nombre username.
    - DELETE "username"/ : Elimina el usuario con nombre username.
    - GET "username"/artists/ : Devuelve el usuario y un listado con información sobre todos sus artistas.
    - GET "username"/songs/ : Devuelve el usuario y un listado con información sobre todas sus canciones.

Para probar los endpoints, en la raíz del proyecto hay un fichero llamado "PruebaEndpoints.postman_collection.json" que se puede importar en Postman.

### API de spotify
Esta vez el usuario debe insertar ids válidos de canciones y artistas, por tanto no hay que hacer la búsqueda de canciones mediante su nombre para obtener el id. Además, se ha usado otro endpoint para poder obtener múltiples canciones o artistas en una sola llamada, a diferencia de la versión de la unidad 2 donde se tenía que hacer una llamada con cada id. La información que se obtiene es la siguiente:
1. Para los artistas:
    - id
    - nombre
    - seguidores
    - popularidad
    - géneros
    - url a su página de Spotify
2. Para las canciones:
    - id
    - nombre
    - duración en milisegundos
    - popularidad
    - url a su página de Spotify
    - artistas:
        - id
        - nombre
        - fecha de lanzamiento
        - tipo de album
        - cuantas canciones tiene el album
        - url a su página de Spotify
    - álbum:
        - id
        - nombre
        - tipo de álbum
        - número de canciones
        - fecha de lanzamiento
        - url a su página de Spotify

Para hacer uso de esta API hay que solicitar un token que solo tiene una vida de una hora. Por tanto, hay que comprobar que el token es válido, de lo contrario se obtiene uno nuevo. A diferencia de la anterior entrega, esta vez guardo el token y su tiempo de expiración en cache.

### Test
Hay una serie de test que verifican el buen funcionamiento de los endpoints. Para ejecutarlo hay que usar la siguiente instrucción:

```
py .\manage.py test
```

Como hay una versión con apiview y otra con viewset, se ha duplicado el código en ambos test cambiando la ruta.

### Conclusión
Los principales cambios respecto a la versión en Flask consisten en la ampliación del modelo de usuario, al que se le han añadido dos atributos adicionales para enriquecer la información almacenada. Aunque actualmente no son de mucha utilidad, Django facilita mucho su implementación, ya que el propio framework se encarga de la validación y gestión de los modelos. Además, se he decidido almacenar únicamente los identificadores de canciones y artistas de Spotify, una solución menos amigable para el usuario que solo use el backend, pero más adecuada desde el punto de vista técnico, ya que en un escenario con frontend sería este el encargado de gestionar dichos identificadores.\
La validación de datos y gran parte del manejo de errores son gestionados automáticamente por Django, devolviendo mensajes claros cuando la información no es correcta, aunque en algunos casos concretos ha sido necesario implementar lógica adicional. En cuanto a la base de datos, se ha utilizado SQLite, como en el ejercicio anterior, aprovechando el uso de JSONField(default=list) para almacenar canciones y artistas de forma más cómoda y sin necesidad de serialización manual.\
Por último, cabe destacar que no había trabajado previamente con Django y, para alguien que empieza desde cero, no es especialmente intuitivo y hasta que no haces pruebas con la sintaxis parece muy "mágico". Esto hace que la curva de aprendizaje sea más pronunciada al principio, sin embargo, una vez superada esta fase, se aprecia claramente el ahorro de tiempo que ofrece el framework, especialmente al utilizar viewset, ya que se evita tener que gestionar manualmente cada endpoint, su validación y el acceso a la base de datos, como ocurre en Flask o FastAPI. Aun así, considero muy valioso conocer los tres frameworks, ya que cada uno presenta puntos fuertes y débiles que los hacen adecuados para distintos escenarios.
