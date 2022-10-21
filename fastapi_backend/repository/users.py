import database

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from schemas import user_info, department, grade, user_auth
from models import Users
from security.hashing import Hash

get_db = database.get_db

# 회원 가입
def create(user_info: user_info, department: department, grade: grade, auth: user_auth, db: Session):
    # Password Hashing
    hashing_pw = Hash.bcrypt(user_info.password)

    new_user = Users(
        uid = user_info.uid,
        password = hashing_pw,
        email = user_info.email,
        phonenumber = user_info.phonenumber,
        department = department.value,
        grade = grade.value,
        auth = auth.value
        )

    # 관리자 권한 우회 방지
    if new_user.auth == "0":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="사용할 수 없는 권한입니다.")

    # 학번 입력 확인
    if len(str(new_user.uid)) != 7:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="학번을 정확히 입력하세요.")

    # 학번 중복 확인
    uid_count = db.query(Users).filter(Users.uid == user_info.uid).count()
    if uid_count >= 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="학번 중복입니다.")

    # email 중복 확인
    if db.query(Users).filter(Users.email == new_user.email).count():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이메일 중복입니다.")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "생성되었습니다."