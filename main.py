from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.controllers import message_router, admin_router, tarantool_router
from app.controllers.citus_resharding_controller import (
    router as citus_resharding_router,
)
from app.core.db_manager import db_manager
from app.core.tarantool_manager import (
    get_tarantool_connection,
    close_tarantool_connection,
)
from app.core.exceptions import AppError
from app.core.exception_handlers import (
    app_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
from app.middleware import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_manager.connect()
    get_tarantool_connection()
    yield
    # Shutdown
    await db_manager.close()
    close_tarantool_connection()


app = FastAPI(title="Messages Service", version="1.0.0", lifespan=lifespan)

# Middleware
app.add_middleware(RequestIDMiddleware)

# Include routers
app.include_router(message_router, prefix="/api/v1")
app.include_router(tarantool_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(citus_resharding_router, prefix="/api/v1")

# Exception handlers
app.add_exception_handler(AppError, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
