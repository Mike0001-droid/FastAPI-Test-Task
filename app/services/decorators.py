def route(path: str, method: str = "get", response_model=None):
    def decorator(func):
        func._route_info = {
            'path': path,
            'method': method,
            'response_model': response_model
        }
        return func
    return decorator

def get(path: str, response_model=None):
    return route(path, "get", response_model)

def post(path: str, response_model=None):
    return route(path, "post", response_model)

def put(path: str, response_model=None):
    return route(path, "put", response_model)

def delete(path: str, response_model=None):
    return route(path, "delete", response_model)