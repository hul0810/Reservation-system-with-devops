from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import reservation_schema
from repository import reservation
import database

get_db = database.get_db

router = APIRouter(
    prefix="/reservation",
    tags=["예약"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def list_all(db: Session = Depends(get_db)):
    """
    `예약 전체 현황 API`\n
    :return:
    """
    return reservation.list_all(db)

# 예약 현황
@router.get("/{ruser}", status_code=status.HTTP_200_OK)
def list(ruser: str, db: Session = Depends(get_db)):
    """
    `예약 현황 API`\n
    :param ruser:
    :return:
    """
    return reservation.list(ruser, db)

# 예약하기
@router.post("/", status_code=status.HTTP_201_CREATED)
def register(request: reservation_schema, db: Session = Depends(get_db)):
    """
    `예약 API`\n
    :param ruser:
    :param fid:
    :param rstarttime:
    :param rendtime:
    :param rcontents:
    :param attendees:
    :return:\n
    ruser: 7자리
    """
    return reservation.register(request, db)

# 예약 취소
@router.delete("/{rid}", status_code=status.HTTP_204_NO_CONTENT)
def cancel(rid: int, db: Session = Depends(get_db)):
    """
    `예약 취소 API`\n
    :param rid:
    :return:
    """
    return reservation.cancel(rid, db)