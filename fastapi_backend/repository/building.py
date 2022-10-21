import os
import shutil

from schemas import building_schema, building_update_schema
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models import Building
from common.consts import FILE_PATH

file_ext = ['.jpg', '.jpeg', '.gif', '.png']

# Read All
def read_all(db: Session):
    building_list = db.query(Building).all()
    for col in building_list:
        col.bimage = "http://192.168.16.28:30800/building/image/" + col.bid
    return building_list

# Read One
def read_one(bid: str, db: Session):
    one_building = db.query(Building).filter(Building.bid == bid).first()
    if not one_building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"존재하지 않습니다.")
    one_building.bimage = "http://192.168.16.28:30800/building/image/" + one_building.bid
    return one_building

# Create
def create(request: building_schema, bimage, db: Session):
    
    # 입력값 검증
    if not len(request.bid) == 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물ID는 3자리여야 합니다.")
    if " " in request.bid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물 ID는 공백을 넣을 수 없습니다.")
    ## bid 중복 확인
    bid_duplicate_check = db.query(Building).filter(Building.bid == request.bid).count()
    if bid_duplicate_check >= 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="건물ID 중복입니다.")
    
    ## bname 중복 확인
    bname_duplicate_check = db.query(Building).filter(Building.bname == request.bname).count()
    if bname_duplicate_check >= 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="해당 건물은 이미 존재합니다.")
    
    if request.bname.isspace():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물명을 입력하세요.")
    if request.bid == "" or request.bname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물ID 또는 건물 명이 없습니다.")


    # bimage 경로 지정 & 파일 확장자 검증
    if bimage is None:
        file_path = None
    else:
        if bimage.filename[-4:] in file_ext:
            file_path = f"{FILE_PATH}/building/{bimage.filename}"
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only jpg, jpeg, gif, png")
    
    new_building = Building(bid=request.bid, bname=request.bname, bimage=file_path, bcontents=request.bcontents)
    db.add(new_building)
    db.commit()
    db.refresh(new_building)

    if hasattr(bimage, "filename"):
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(bimage.file, buffer)
    
    return "생성되었습니다."

# Update
def update(bid: str, request: building_update_schema, bimage, db: Session):
    
    # 입력값 검증
    if request.bname.isspace():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물명을 입력하세요.")
    if request.bname == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="건물ID 또는 건물 명이 없습니다.")
    building_update = db.query(Building).filter(Building.bid == bid)
    if not building_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않습니다.}")

    # 에러 처리
    
    ## bname 중복 확인
    bname_pulicate_check = db.query(Building).filter(Building.bname == request.bname).count()
    if bname_pulicate_check >= 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="해당 건물은 이미 존재합니다.")

    # bimage 경로 지정 & 파일 확장자 검증

    if bimage is None:
        file_path = None
    else:
        if bimage.filename[-4:] in file_ext:
            file_path = f"{FILE_PATH}/building/{bimage.filename}"
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="only jpg, jpeg, gif, png")
    data = request.dict()
    data['bimage'] = file_path

    building_update.update(data)
    db.commit()

    if hasattr(bimage, "filename"):
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(bimage.file, buffer)

    return "수정되었습니다."

# Delete
def delete(bid: str, db: Session):
    building_one = db.query(Building).filter(Building.bid == bid).first()
    if not building_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"존재하지 않습니다.")
    db.delete(building_one)
    db.commit()

    if building_one.bimage is not None:
        os.remove(f'{building_one.bimage}')

# Get Image
def get_image(bid: str, db: Session):
    col = db.query(Building).filter(Building.bid == bid).first()

    # 건물 존재 확인
    bid_check = db.query(Building).filter(Building.bid == bid).count()
    if bid_check == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 건물은 존재하지 않습니다.")

    # 이미지 유무 처리
    if col.bimage is None:
        return {"detail": "No image"}
    else:
        return FileResponse(f"{col.bimage}")