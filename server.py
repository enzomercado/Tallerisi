
import json
from wsgiref.simple_server import make_server


tasks = {}         
next_id = 1          



def read_json_body(environ):
   
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        length = 0

    if length == 0:
        return {}

    raw_body = environ["wsgi.input"].read(length)
    return json.loads(raw_body.decode("utf-8"))


def json_response(start_response, status, payload=None):
   
    if payload is None:
        body = b""
    else:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body))),
    ]
    start_response(status, headers)
    return [body]


def parse_path(path):
   
    parts = [p for p in path.split("/") if p != ""]

    if len(parts) == 1 and parts[0] == "tasks":
        return "tasks", None

    if len(parts) == 2 and parts[0] == "tasks":
        try:
            task_id = int(parts[1])
        except ValueError:
            return None, None
        return "tasks", task_id

    return None, None

def handle_get(start_response, task_id):
    if task_id is None:
        
        return json_response(start_response, "200 OK", list(tasks.values()))

   
    task = tasks.get(task_id)
    if task is None:
        return json_response(
            start_response, "404 Not Found", {"error": "task not found"}
        )
    return json_response(start_response, "200 OK", task)


def handle_post(environ, start_response):
    global next_id

    try:
        data = read_json_body(environ)
    except (ValueError, json.JSONDecodeError):
        return json_response(
            start_response, "400 Bad Request", {"error": "invalid JSON body"}
        )

    task = dict(data)  
    task["id"] = next_id
    tasks[next_id] = task
    next_id += 1

    return json_response(start_response, "201 Created", task)


def handle_patch(environ, start_response, task_id):
    if task_id is None:
        return json_response(
            start_response, "404 Not Found", {"error": "task not found"}
        )

    task = tasks.get(task_id)
    if task is None:
        return json_response(
            start_response, "404 Not Found", {"error": "task not found"}
        )

    try:
        changes = read_json_body(environ)
    except (ValueError, json.JSONDecodeError):
        return json_response(
            start_response, "400 Bad Request", {"error": "invalid JSON body"}
        )

    
    task.update(changes)
    task["id"] = task_id  

    return json_response(start_response, "200 OK", task)


def handle_delete(start_response, task_id):
    if task_id is None or task_id not in tasks:
        return json_response(
            start_response, "404 Not Found", {"error": "task not found"}
        )

    del tasks[task_id]
    
    start_response("204 No Content", [])
    return [b""]


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")

    resource, task_id = parse_path(path)

    if resource != "tasks":
        return json_response(
            start_response, "404 Not Found", {"error": "resource not found"}
        )

    if method == "GET":
        return handle_get(start_response, task_id)

    if method == "POST":
        if task_id is not None:
            
            return json_response(
                start_response,
                "405 Method Not Allowed",
                {"error": "POST is only allowed on /tasks"},
            )
        return handle_post(environ, start_response)

    if method == "PATCH":
        return handle_patch(environ, start_response, task_id)

    if method == "DELETE":
        return handle_delete(start_response, task_id)


    return json_response(
        start_response,
        "405 Method Not Allowed",
        {"error": f"method {method} not allowed"},
    )


if __name__ == "__main__":
    host, port = "localhost", 9292
    with make_server(host, port, app) as httpd:
        print(f"Sirviendo en http://{host}:{port} (Ctrl+C para detener)")
        httpd.serve_forever()
