from fastapi import FastAPI
import routes.auth_route.auth_route as _auth
import routes.auth_route.passord_route as _psw
import routes.jobs_route.job_route as _job
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
        debug=True,
        title= "School Management System",
        openapi_url="/school.json"
    )


origins = [
    "http://localhost:8090",
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
app.include_router(_job.job, tags=["Apply Job"])