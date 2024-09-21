from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.exceptions import CoreException

from account.api.authentication import authenticationR

app = FastAPI(title='SimbirHealth account')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

apiRouter = APIRouter(prefix='/api', tags=['api'])


@apiRouter.get('/ping')
async def ping():
    return 'pong'


apiRouter.include_router(authenticationR)

@app.exception_handler(CoreException)
async def exception_handler(res, exc: CoreException):
    return JSONResponse({'error': exc.message})


app.include_router(apiRouter)
