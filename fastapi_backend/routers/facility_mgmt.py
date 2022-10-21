import database

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from schemas import facility_schema, facility_update_schema
from repository import facility
from security.oauth2 import get_current_user

get_db = database.get_db

router = APIRouter(
    prefix="/facility",
    tags=["관리자용 - 시설물 관리"]
)

# Read All
@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: Session = Depends(get_db)):
    """
    `시설물 리스트 API`\n
    :return:
    """
    return facility.read_all(db)

# Read One
@router.get("/{fid}", status_code=status.HTTP_200_OK)
def read_one(fid: str, db: Session = Depends(get_db), auth: str = Depends(get_current_user)):
    """
    `시설물 API`\n
    :param fid:
    :return:
    """
    return facility.read_one(fid, db)

# Create
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        request: facility_schema = Depends(facility_schema.as_form),
        fimage: UploadFile = File(None),
        db: Session = Depends(get_db), 
        auth: str = Depends(get_current_user),
    ):
    """
    `시설물 등록 API`\n
    :param fid:
    :param fname:
    :param fcontents:
    :param fimage:
    :param bid:
    :param ftypeid:
    :return:\n
    fid: 4자리 (PK)\n
    bid: 3자리 (FK)
    """
    return facility.create(request, fimage, db)

# Update
@router.put("/{fid}", status_code=status.HTTP_202_ACCEPTED)
def update(
        fid: str,
        request: facility_update_schema = Depends(facility_update_schema.as_form),
        fimage: UploadFile = File(None),
        db: Session = Depends(get_db),
        auth: str = Depends(get_current_user)
    ):
    """
    `정보 수정 API`\n
    :param fid:
    :param fname:
    :param fimage:
    :param fcontents:
    :return:\n
    bid: 4자리 (FK)\n
    ftypeid: 2자리 (FK)
    """
    return facility.update(fid, request, fimage, db)

# Delete
@router.delete("/{fid}", status_code=status.HTTP_204_NO_CONTENT)
def delete(fid: str, db : Session = Depends(get_db), auth: str = Depends(get_current_user)):
    """
    `삭제 API`\n
    :param fid:
    :return:
    """
    return facility.delete(fid, db)

# Get Image
@router.get("/image/{fid}")
async def get_image(fid: str, db: Session = Depends(get_db)):
    """
    `Image 파일 API`\n
    :param fid:
    :return:
    """
    return facility.get_image(fid, db)