from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.exceptions import BaseExceptions, ConflictError, NotFoundError

from timetable.api.timetable import timetableR
from timetable.api.appointment import appointmenteR

app = FastAPI(title='SimbirHealth timetable')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

apiRouter = APIRouter(prefix='/api')

apiRouter.include_router(timetableR)
apiRouter.include_router(appointmenteR)


@app.exception_handler(BaseExceptions)
async def exception_handler(res, exc: BaseExceptions):
    status = 400
    if isinstance(exc, ConflictError):
        status = 409
    elif isinstance(exc, NotFoundError):
        status = 404
    return JSONResponse({'error': exc.message}, status_code=status)



app.include_router(apiRouter)
