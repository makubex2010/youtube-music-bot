from aiogram import Router

from .commands_handler import router as command_router
from .favorite_handler import router as favorite_router
from .main_handler import router as main_router

router = Router()

router.include_routers(
    command_router,
    main_router,
    favorite_router,
)
