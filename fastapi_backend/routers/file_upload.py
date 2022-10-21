import shutil

from fastapi import APIRouter, FastAPI, File, UploadFile, Depends
from fastapi.responses import FileResponse
from common.consts import FILE_PATH, PROJECT_ROOT_DIR
from schemas import building_schema
from repository.multipart_form import as_form

router = APIRouter(
    prefix="/fileupload",
    tags=["File_Upload_Test"]
)

app = FastAPI()

@router.get("/file")
async def get_file(filename: str):
    file_path = FILE_PATH
    return FileResponse(f"{FILE_PATH}/building/{filename}")

@router.post("/uploadfile/")
async def create_upload_file(form: building_schema = Depends(building_schema.as_form), file: UploadFile = File(...)):
    with open(f'{FILE_PATH}/{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "filename": file.filename,
        }
