import database
import ntpath # 리눅스는 posixpath 다

from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas import building_schema, building_update_schema
from repository import building
from security.oauth2 import get_current_user

get_db = database.get_db

router = APIRouter(
    prefix="/building",
    tags=["관리자용 - 건물 관리"]
)

# Read All
@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: Session = Depends(get_db)):
    """
    `건물 리스트 API`\n
    :return:
    """
    return building.read_all(db)

# Read One
@router.get("/{bid}", status_code=status.HTTP_200_OK)
def read_one(bid: str, db: Session = Depends(get_db), auth: str = Depends(get_current_user)):
    """
    `건물 API`\n
    :param bid:
    :return:
    """
    return building.read_one(bid, db)

# Create
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        request: building_schema = Depends(building_schema.as_form),
        bimage: UploadFile = File(None),
        db: Session = Depends(get_db), 
        auth: str = Depends(get_current_user)
    ):
    """
    `건물 등록 API`\n
    :param bid:
    :param bname:
    :param bimage:
    :param bcontents:
    :return:\n
    bid: 3자리 (PK)
    """
    return building.create(request, bimage, db)

# Update
@router.put("/{bid}", status_code=status.HTTP_202_ACCEPTED)
def update(
        bid: str,
        request: building_update_schema = Depends(building_update_schema.as_form),
        bimage: UploadFile = File(None),
        db: Session = Depends(get_db), 
        auth: str = Depends(get_current_user)
    ):
    """
    `정보 수정 API`\n
    :param bid:
    :param bname:
    :param bimage:
    :param bcontents:
    :return:
    """
    return building.update(bid, request, bimage, db)

# Delete
@router.delete("/{bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete(bid: str, db: Session = Depends(get_db), auth: str = Depends(get_current_user)):
    """
    `삭제 API`\n
    :param bid:
    """
    return building.delete(bid, db)

# Get Image
@router.get("/image/{bid}")
async def get_image(bid: str, db: Session = Depends(get_db)):
    """
    `Image 파일 API`\n
    :param bid:
    :return:
    """
    return building.get_image(bid, db)