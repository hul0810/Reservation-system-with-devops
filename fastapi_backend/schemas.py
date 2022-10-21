from pydantic import BaseModel, EmailStr
# from pydantic.networks import EmailStr
from typing import Optional
from datetime import datetime

from enum import Enum

from repository.multipart_form import as_form

# Building Schema
@as_form
class building_schema(BaseModel):
    bid: str
    bname: str
    # bimage: Optional[str] = None
    bcontents: Optional[str] = None

@as_form
class building_update_schema(BaseModel):
    bname: str
    # bimage: Optional[str] = None
    bcontents: Optional[str] = None


# Facility Schema
@as_form
class facility_schema(BaseModel):
    fid: str
    fname: str
    fcontents: Optional[str] = None
    # fimage: Optional[str] = None
    bid: str
    ftypeid: str

@as_form
class facility_update_schema(BaseModel):
    fname: str
    fcontents: Optional[str] = None
    # fimage: Optional[str] = None
    bid: str
    ftypeid: str

# Users
class user_info(BaseModel):
    uid: int
    password: str
    email: EmailStr
    phonenumber: str
    # bid: Optional[str] = None

# Users - department
class department(Enum):
    admin = "관리자"
    CyberSec = "사이버보안과"
    Nursing = "간호학과"
    Machinery = "기계과"
    Electronics = "전자과"

# Users - grade
class grade(Enum):
    admin = "관리자"
    freshman = "1학년"
    sophomore = "2학년"
    junior = "3학년"
    senior = "4학년"

# Users - auth
class user_auth(Enum):
    admin: str = "0"
    Professor: str = "1" 
    student: str = "2"
    etc: str = "3"

# Reservation
class reservation_schema(BaseModel):
    ruser: str # 예약자 이름
    fid: str # 예약 시설명
    rstarttime: datetime # 예약 시간 (예약 시작 시간)
    rendtime: datetime # 예약 시간 (예약 종료 시간)
    rcontents: str # 추가 내용
    attendees: str # 참석자 명

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# GraphQL
# class building_gql(SQLAlchemyObjectType):
#     class Meta:
#         model = Building     
# SQLAlchemyObjectType 사용 시 session을 close할 방법을 모르겠음