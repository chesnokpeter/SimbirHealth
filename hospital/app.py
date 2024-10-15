from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.exceptions import RestExceptions

from hospital.api.hospitals import hospitalsR


app = FastAPI(title='SimbirHealth hospitals')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

apiRouter = APIRouter(prefix='/api')

apiRouter.include_router(hospitalsR)


@app.exception_handler(RestExceptions)
async def exception_handler(res, exc: RestExceptions):
    return JSONResponse({'error': exc.message}, 400)


app.include_router(apiRouter)
