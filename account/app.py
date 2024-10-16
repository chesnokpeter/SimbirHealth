from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from account.exceptions import ErrorModel
from core.exceptions import BaseExceptions, ConflictError, NotFoundError

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
apiRouter.responses = {
    400: {"model":ErrorModel,"description": "Ошибка при обработке данных"},
    404: {"model":ErrorModel,"description": "Ресурс не найден"},
    409: {"model":ErrorModel,"description": "Ошибка конфликта"}
}

apiRouter.include_router(authenticationR)
apiRouter.include_router(accountsR)
apiRouter.include_router(doctorsR)



@app.exception_handler(BaseExceptions)
async def exception_handler(res, exc: BaseExceptions):
    status = 400
    if isinstance(exc, ConflictError):
        status = 409
    elif isinstance(exc, NotFoundError):
        status = 404
    return JSONResponse({'error': exc.message}, status_code=status)


app.include_router(apiRouter)
