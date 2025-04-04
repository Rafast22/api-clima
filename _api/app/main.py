from fastapi import FastAPI, APIRouter, BackgroundTasks
from .routers import user, auth, cultivo, localidad, historico, previcion
from fastapi.responses import RedirectResponse
from .database import get_db,Base,engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .interceptor.predict import predict
from .interceptor.nasa_request import get_history_date, get_new_history_date
from ._schemas.localidad import RequestLocalidadCreate
from ._models.localidad import Localidad
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from fastapi import Depends
router = APIRouter()
# templates = Jinja2Templates(directory="/home/rafa/Projects/Python/api-clima/frontend/dist/front/browser/")

origins = [
    "http://localhost:8080",
    "http://localhost:4200",
    "*"
 ]


#adicionar a funncao que vai atualizar as previcoes da localizacao de los cedrales
#adicionar o cron pra atualiazr a lista
#limpar os registro de lixo que ja passaram?
#adicionar a atualizacao do modelo com as informaceos da nasa
#fazer novas previsoes

#update_model_data
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Base.metadata.create_all(bind=engine)

    # inspector = inspect(engine)
    # if inspector.has_table("User"):
    #     Base.metadata.drop_all(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    yield
    
async def fetch_request(db):

    db_localidades = Localidad.get_by_latitude_longitude(db, "-25.65", "-54.70")
    if len(db_localidades) > 0:
        db_localidad = db_localidades[0]
    if not db_localidad:
        new = RequestLocalidadCreate(**{'latitude':'-25.65', 'longitude':'-54.70', 'user_id':None, 'cultivo_id':None} )
        db_localidad = Localidad.create(db, **new.model_dump())
    
    h = await get_history_date(db_localidad.latitude, db_localidad.longitude)
    predict(db, h, db_localidad)
    del h, db_localidad


app = FastAPI(lifespan=lifespan)    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="../frontend/dist/front/browser/"), name="static")
# scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_request, 'cron', hour=0, minute=0, args=(get_db()))
scheduler.start()

# @router.get("/")
# async def root(request: Request):
    
#     return templates.TemplateResponse("index.html", {"request": request})

@router.get("/test/preditct")
async def f(db: Session = Depends(get_db)):
    await fetch_request(db)

app.include_router(router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cultivo.router)
app.include_router(historico.router)
app.include_router(localidad.router)
app.include_router(previcion.router)




