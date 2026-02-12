print("this is main file")


from fastapi import FastAPI
from app.database.db import engine , Base
from app.models import user
from app.routes import auth
from app.routes import repo as route_repo
from app.models import repo
from app.models import commit
from app.utils.scheduler import start_scheduler

app = FastAPI(title="github release monitor")

print("app started now tables are creating")
Base.metadata.create_all(bind=engine)   
print("table created")




app.include_router(auth.router)
app.include_router(route_repo.router)


@app.get("/")
def root():
    return {
        "message" : "root is working"
    }

@app.on_event("startup")
def startup_event():
    start_scheduler()

