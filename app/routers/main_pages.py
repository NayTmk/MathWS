from fastapi import APIRouter, Request

from app.core.config import settings
from app.domain.game_managers import task_manager
from app.utils.deps import CurrentUser, SessionDep

router = APIRouter()


@router.get('/')
async def main_page(
        request: Request, user: CurrentUser, session: SessionDep
):
    operations = task_manager.get_operators_with_desc()
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='main_page.html',
        context={'user': user, 'operations': operations}
    )