from database import db_session
from models import Users
from security.hashing import Hash

def admin_create():
    Session = db_session()

    hashing_pw = Hash.bcrypt('ycdc2021')

    new_user = Users(
        uid = 0,
        password = hashing_pw,
        email = "admin@admin.com",
        phonenumber = "01012345678",
        department = "관리자",
        grade = "관리자",
        auth = "0"
        )

    try:
        if Session.query(Users).filter(Users.email == "admin@admin.com").first():
            return
        else:
            Session.add(new_user)
            Session.commit()
            Session.refresh(new_user)
    finally:
        Session.close()
        

print(Hash.bcrypt("ycdc2021"))
