#

## Rutas

* `GET /tasks` → muestra todas las tareas.
* `GET /tasks/{id}` → muestra una tarea específica.
* `POST /tasks` → crea una tarea nueva.
* `PATCH /tasks/{id}` → modifica los datos de una tarea.
* `DELETE /tasks/{id}` → elimina una tarea.
* Si la ruta no existe devuelve `404`, y si el verbo no está permitido devuelve `405`.

## Verbos HTTP

* **GET:** se usa para consultar información. No modifica las tareas, solamente las muestra.
* **POST:** se usa para crear una tarea nueva. Cada vez que se hace un POST se crea una tarea diferente.
* **PATCH:** se usa para modificar una tarea que ya existe. Permite cambiar solamente los campos que se envían.
* **DELETE: **se usa para eliminar una tarea. Si la tarea no existe, devuelve `404`.

## Pruebas

Las pruebas se pueden hacer con el script `demo-verbos-http.sh`. La salida se puede guardar en `evidencia.txt`.
