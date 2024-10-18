from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.exceptions import ServiceException, ConflictError, NotFoundError

from hospital.api.hospitals import hospitalsR
from hospital.exceptions import ErrorModel, JWTExceptions

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
apiRouter.responses = {
    400: {"model":ErrorModel,"description": "Некорректные данные в запросе"},
    401: {"model":ErrorModel,"description": "Токен недействителен или срок его действия истёк"},
    403: {"model":ErrorModel,"description": "Нет доступа"},
    404: {"model":ErrorModel,"description": "Ресурс не найден"},
    409: {"model":ErrorModel,"description": "Конфликт данных"}
}
apiRouter.include_router(hospitalsR)

@app.exception_handler(ServiceException)
async def exception_handler(res, exc: ServiceException):
    status = 400
    if isinstance(exc, ConflictError):
        status = 409
    elif isinstance(exc, NotFoundError):
        status = 404
    elif isinstance(exc, JWTExceptions):
        status = 401
    elif isinstance(exc, PermissionError):
        status = 403
    return JSONResponse({'error': exc.message}, status_code=status)


app.include_router(apiRouter)
