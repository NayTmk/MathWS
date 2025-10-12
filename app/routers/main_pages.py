from fastapi import APIRouter, Request

from app.config import settings
from app.utils.deps import CurrentUser


router = APIRouter()


@router.get('/')
async def main_page(
        request: Request, user: CurrentUser
):
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='main_page.html',
        context={'user': user, 'operations': {'a': 'b'}}
    )