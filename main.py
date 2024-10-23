from fastapi import FastAPI
import routes.auth_routes.auth_route as _auth
import routes.auth_routes.passord_route as _psw
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
        debug=True,
        title= "School Management System",
        openapi_url="/openapi.json"
    )


origins = [
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(_auth.auth, tags=["Authentication"])
app.include_router(_psw.psw, tags=["Forget Password"])