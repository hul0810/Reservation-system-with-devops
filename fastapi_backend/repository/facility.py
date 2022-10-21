import os
import shutil

from schemas import facility_schema, facility_update_schema
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models import Facility, Building, FacilityType
from common.consts import FILE_PATH

file_ext = ['.jpg', '.jpeg', '.gif', '.png']

# Read All
def read_all(db: Session):
    facility_list = db.query(Facility).all()
    for col in facility_list:
        col.fimage = "http://192.168.16.28:30800/facility/image/" + col.fid
    return facility_list

# Read One
def read_one(fid: str, db: Session):
    one_facility = db.query(Facility).filter(Facility.fid == fid).first()
    one_facility.fimage = "http://192.168.16.28:30800/facility/image/" + one_facility.fid
    if not one_facility:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"존재하지 않습니다.")
    return one_facility

# Create
def create(request: facility_schema, fimage, db: Session):

    # 입력값 검증
    if not len(request.fid) == 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물 ID는 4자리여야 합니다.")
    if not len(request.bid) == 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물 ID는 3자리여야 합니다.")
    
    ## fid 중복 확인
    fid_duplicate_check = db.query(Facility).filter(Facility.fid == request.fid).count()
    if fid_duplicate_check >= 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="시설물ID 중복입니다.")
    
    ## bid FK
    bid_FK = db.query(Building).filter(Building.bid == request.bid).count()
    if bid_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 BID는 존재하지 않습니다.")
    
    if not len(request.ftypeid) == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물 종류 ID는 2자리여야 합니다.")
    
    ## ftypeid FK
    ftypeid_FK = db.query(FacilityType).filter(FacilityType.ftypeid == request.ftypeid).count()
    if ftypeid_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 FTYPEID는 존재하지 않습니다.")
    
    if " " in request.fid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물 ID는 공백을 넣을 수 없습니다.")
    if request.fname.isspace():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물명을 입력하세요.")
    if request.fid == "" or request.fname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물 ID 또는 시설물명이 없습니다.")

    # fimage 경로 지정 & 파일 확장자 검증

    if fimage is None:
        file_path = None
    else:
        if fimage.filename[-4:] in file_ext:
            file_path = f"{FILE_PATH}/facility/{fimage.filename}"
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only jpg, jpeg, gif, png")

    new_facility = Facility(
                fid=request.fid,
                fname=request.fname,
                fimage=file_path,
                fcontents=request.fcontents,
                bid=request.bid,
                ftypeid=request.ftypeid
                )

    db.add(new_facility)
    db.commit()
    db.refresh(new_facility)

    if hasattr(fimage, "filename"):
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(fimage.file, buffer)

    return "생성되었습니다."

# Update
def update(fid: str, request: facility_update_schema, fimage, db: Session):
    
    # 입력값 검증
    if request.fname.isspace():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물명을 입력하세요.")
    if request.fname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="시설물 ID 또는 시설물명이 없습니다.")
    facility_update = db.query(Facility).filter(Facility.fid == fid)
    if not facility_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않습니다.}")

    # FK 에러 처리

    ## bid FK
    bid_FK = db.query(Building).filter(Building.bid == request.bid).count()
    if bid_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 BID는 존재하지 않습니다.")

    ## ftypeid FK
    ftypeid_FK = db.query(FacilityType).filter(FacilityType.ftypeid == request.ftypeid).count()
    if ftypeid_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 FTYPEID는 존재하지 않습니다.")

    ## fimage 경로 지정 & 파일 확장자 검증
    
    if fimage is None:
        file_path = None
    else:
        if fimage.filename[-4:] in file_ext:
            file_path = f"{FILE_PATH}/facility/{fimage.filename}"
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only jpg, jpeg, gif, png")
    
    data = request.dict()
    data['fimage'] = file_path

    facility_update.update(data)
    db.commit()

    if hasattr(fimage, "filename"):
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(fimage.file, buffer)

    return "수정되었습니다."

# Delete
def delete(fid: str, db: Session):
    facility_one = db.query(Facility).filter(Facility.fid == fid).first()
    if not facility_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"존재하지 않습니다.")
    db.delete(facility_one)
    db.commit()

    if facility_one.fimage is not None:
        os.remove(f'{facility_one.fimage}')

# Get Image
def get_image(fid: str, db: Session):
    col = db.query(Facility).filter(Facility.fid == fid).first()

    # 시설물 존재 확인
    fid_check = db.query(Facility).filter(Facility.fid == fid).count()
    if fid_check == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 시설물은 존재하지 않습니다.")

    # 이미지 유무 처리
    if col.fimage is None:
        return {"detail": "No image"}
    else:
        return FileResponse(f"{col.fimage}")

