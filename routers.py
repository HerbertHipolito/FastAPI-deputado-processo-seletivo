from fastapi import APIRouter
from controllers import deputado_controller

router = APIRouter()

router.include_router(deputado_controller.router)