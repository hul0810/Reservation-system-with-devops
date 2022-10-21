import database

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models import FacilityType

get_db = database.get_db

router = APIRouter(
    prefix="/ftype",
    tags=["시설물 종류"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def list(db: Session = Depends(get_db)):
    """
    `시설물 타입 API`\n
    :return:
    """
    ftype_list = db.query(FacilityType).all()
    return ftype_list