import sys

from fastapi import APIRouter, status

import api.v1.pays.services as _services
from core.utils.responses import EnvelopeResponse

sys.path.append("....")
from db.session import get_session  # noqa: E402

router = APIRouter(prefix="/pays", tags=["Pays"])


@router.get("/List", status_code=status.HTTP_200_OK, summary="Pays list.", response_model=EnvelopeResponse)
async def get_pays() -> EnvelopeResponse:
    db = next(get_session())
    result = await _services.get_all_pays(db)
    db.close()
    return EnvelopeResponse(errors=None, body={"pays": result})
