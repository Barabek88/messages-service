from app.controllers.message_controller import router as message_router
from app.controllers.message_controller import tarantool_router
from app.controllers.admin_controller import router as admin_router

__all__ = ["message_router", "admin_router", "tarantool_router"]
