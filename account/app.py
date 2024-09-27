from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.exceptions import RestExceptions

from account.api.authentication import authenticationR
from account.api.accounts import accountsR
from account.api.doctors import doctorsR

app = FastAPI(title='SimbirHealth account')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

apiRouter = APIRouter(prefix='/api')

apiRouter.include_router(authenticationR)
apiRouter.include_router(accountsR)
apiRouter.include_router(doctorsR)

@app.exception_handler(RestExceptions)
async def exception_handler(res, exc: RestExceptions):
    return JSONResponse({'error': exc.message}, 400)


app.include_router(apiRouter)
