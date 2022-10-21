from datetime import datetime

from fastapi import status, HTTPException
from sqlalchemy.sql.expression import and_
from sqlalchemy.orm import Session

from models import Reservation, Facility, Users

# 예약 현황 
def list_all(db: Session):
    """
    `예약 현황 API`
    """
    # 기능
    reservation_list = db.query(Reservation).order_by(Reservation.rstarttime.asc()).all()
    if not reservation_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않습니다.")
    return reservation_list

# 예약 현황 
def list(ruser: str, db: Session):
    """
    `예약 현황 API`
    """
    # 기능
    one_reservation = db.query(Reservation).filter(Reservation.ruser == ruser).order_by(Reservation.rstarttime).all()

    if not one_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않습니다.")
    return one_reservation


# 예약하기
def register(request: Reservation, db: Session):
    """
    `예약 등록 API`
    """

    # 에러 처리 (fid, ruser, rstarttime, rendtime)
    
    if not request.ruser.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="학번은 숫자만 사용하세요.")

    # 입력값 검증 (fid, ruser, rstarttime, rendtime)
    if not len(request.ruser) == 7:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="학번은 7자리여야 합니다.")
    if not request.ruser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="학번을 입력하세요.")


    # FK 에러 처리 (fid, ruser)

    ## fid FK
    fid_FK = db.query(Facility).filter(Facility.fid == request.fid).count()
    if fid_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 fid는 존재하지 않습니다.")
    
    ## ruser FK
    ruser_FK = db.query(Users).filter(Users.uid == request.ruser).count()
    if ruser_FK == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 ruser는 존재하지 않습니다.")


    # 예약 로직

    ## 현시간 이전 날짜 예약 금지
    currunt_time = datetime.today()
    if request.rstarttime < currunt_time or request.rendtime < currunt_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="예약이 불가능한 날짜입니다.")
    
    ## rstarttime < rendtime
    if request.rstarttime >= request.rendtime:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="종료 시간을 정확히 입력하세요.")

    ## 예약 시간 중복 체크
    time_duplicate_check = db.query(Reservation).filter(
        and_(
            Reservation.rstarttime < request.rendtime,
            Reservation.rendtime > request.rstarttime
            )
        ).filter(Reservation.fid == request.fid).count()

    if time_duplicate_check > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 예약이 있습니다.")

    # 기능
    register = Reservation(
        fid=request.fid,
        ruser=request.ruser,
        rstarttime=request.rstarttime,
        rendtime=request.rendtime,
        rcontents=request.rcontents,
        attendees=request.attendees
        )
    db.add(register)
    db.commit()
    db.refresh(register)
    return "예약되었습니다."

# 예약 취소
def cancel(rid: int, db: Session):
    reservation_delete = db.query(Reservation).filter(Reservation.rid == rid).delete(synchronize_session=False)
    if not reservation_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"존재하지 않습니다.")
    db.commit()

