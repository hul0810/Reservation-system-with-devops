import models

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import (
    login,
    users,
    building_mgmt,
    facility_mgmt,
    reservation,
    facility_type,
)

from database import engine
from repository import admin_create

app = FastAPI()

# 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 관리자 계정 생성 
admin_create.admin_create()

# 미들웨어 정의
origins = [
    "*",
    "http://192.168.16.28:30080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 정의
app.include_router(login.router)
app.include_router(users.router)
app.include_router(building_mgmt.router)
app.include_router(facility_mgmt.router)
app.include_router(reservation.router)
app.include_router(facility_type.router)