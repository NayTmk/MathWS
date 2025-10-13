from fastapi import APIRouter, Request

from app import crud
from app.core.config import settings
from app.utils.deps import CurrentUser, SessionDep

router = APIRouter()


@router.get('/')
async def main_page(
        request: Request, user: CurrentUser, session: SessionDep
):
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='main_page.html',
        context={'user': user, 'operations': {'a': 'b'}}
    )