from sqlalchemy import Column, String, DateTime, BigInteger, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base

class Building(Base):
    __tablename__ = "building"
    __table_args__ = {'schema': 'facility'}
    bid = Column(String(3), primary_key=True, index=True, nullable=False)
    bname = Column(String(10), nullable=False)
    bimage = Column(String(50))
    bcontents = Column(String(300))

    facility = relationship("Facility", back_populates="building")

class FacilityType(Base):
    __tablename__ = "facilitytype"
    __table_args__ = {'schema': 'facility'}
    ftypeid = Column(String(2), primary_key=True, index=True, nullable=False)
    ftypename = Column(String(10), nullable=False)

    facility = relationship("Facility", back_populates="facilitytype")

class Facility(Base):
    __tablename__ = "facility"
    __table_args__ = {'schema': 'facility'}
    fid = Column(String(4), primary_key=True, index=True, nullable=False)
    fname = Column(String(10), nullable=False)
    fcontents = Column(String(300))
    fimage = Column(String(30))
    bid = Column(String(3), ForeignKey('facility.building.bid')) # 스키마.테이블.컬럼
    ftypeid = Column(String(2), ForeignKey('facility.facilitytype.ftypeid')) # 스키마.테이블.컬럼

    building = relationship("Building", back_populates="facility")
    facilitytype = relationship("FacilityType", back_populates="facility")

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'facility'}
    uid = Column(BigInteger, primary_key=True, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(20), nullable=False)
    department = Column(
        Enum("관리자", "사이버보안과", "간호학과", "기계과", "전자과", name="department"),
        nullable=False
        )
    grade = Column(
        Enum("관리자", "1학년", "2학년", "3학년", "4학년", name="grade"),
        nullable=False
        )
    phonenumber = Column(String(11), nullable=False)
    auth = Column(
        Enum("0", "1", "2", "3", name="user_auth"),
        nullable=False
        )
    bid = Column(String(4))

    # reservation = relationship("Reservation", back_populates="users")

class Reservation(Base):
    __tablename__ = "reservation"
    __table_args__ = {'schema': 'facility'}
    rid = Column(BigInteger, primary_key=True, index=True, nullable=False)
    # rname = Column(String(20), nullable=False)
    fid = Column(String(5), nullable=False)
    ruser = Column(BigInteger, nullable=False)
    rstarttime = Column(DateTime, nullable=False)
    rendtime = Column(DateTime, nullable=False)
    rcontents = Column(String(300))
    attendees = Column(String(200))

    # facility = relationship("Facility", back_populates="reservation")
    # users = relationship("Users", back_populates="reservation")


    # department = Column(String(20), nullable=False)
    # grade = Column(String(1), nullable=False)
    # auth = Column(String(1), nullable=False)