from fastapi.responses import JSONResponse

def create_error_response(message: str, data: dict = None, status_code: int = 401) -> JSONResponse:
    response = {
        "success": False,
        "message": message,
        "data": data
    }
    return JSONResponse(status_code=status_code, content=response)