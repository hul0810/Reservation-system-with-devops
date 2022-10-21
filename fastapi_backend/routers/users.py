import database

from fastapi import APIRouter, status, Depends
from schemas import user_info, department, grade, user_auth
from repository import users
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/register",
    tags=["회원가입"]
)

get_db = database.get_db

# Create User
@router.post('/', status_code=status.HTTP_201_CREATED)
def register_user(
    user_info: user_info,
    department: department,
    grade: grade,
    auth: user_auth,
    db: Session = Depends(get_db)
    ):
    """
    `회원가입 API`\n
    :param user_info:
    :param department:
    :param grade:
    :param auth:
    :return:\n
    [0: 관리자, 1: 교수, 2: 학생, 3: 기타]\n
    학번은 7자리 (오로지 숫자만)
    """
    return users.create(user_info, department, grade, auth, db)