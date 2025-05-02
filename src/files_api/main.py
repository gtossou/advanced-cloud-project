import os
from datetime import datetime
from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    FastAPI,
    Request,
    Response,
    UploadFile,
    status,
    APIRouter,
)
from fastapi.responses import StreamingResponse
from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from files_api.s3.write_objects import upload_s3_object
from pydantic import BaseModel

#####################
# --- Constants --- #
#####################

####################################
# --- Request/response schemas --- #
####################################


# read (cRud)
class FileMetadata(BaseModel):
    file_path: str
    last_modified: datetime
    size_bytes: int

class PutFileResponse(BaseModel):
    file_path: str
    message: str

# more pydantic models ...


ROUTER = APIRouter()
##################
# --- Routes --- #
##################

@ROUTER.put("/files/{file_path:path}")
async def upload_file(file_path: str, file: UploadFile, response: Response) -> PutFileResponse: 
    """Upload a file."""
    
    object_already_exists = object_exists_in_s3(
        bucket_name=s3_bucket_name,
        object_key=file_path)
    if object_already_exists:
        response_message = "File already exists at path: /{file_path}"
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        response_message = "File uploaded successfully at path /{file_path}"
        response.status_code = status.HTTP_200_OK
    
    
    file_contents:bytes = await file.read()
    upload_s3_object(
        bucket_name=s3_bucket_name,
        object_key=file_path,
        file_content=file_contents,
        content_type=file.content_type,
    )
    return PutFileResponse(file_path=file_path, message=response_message)


@ROUTER.get("/files")
async def list_files(
    query_params=...,
):
    """List files with pagination."""
    ...


@ROUTER.head("/files/{file_path:path}")
async def get_file_metadata(file_path: str, response: Response) -> Response:
    """Retrieve file metadata.

    Note: by convention, HEAD requests MUST NOT return a body in the response.
    """
    return


@ROUTER.get("/files/{file_path:path}")
async def get_file(
    file_path: str,
) :
    """Retrieve a file."""
    ...


@ROUTER.delete("/files/{file_path:path}")
async def delete_file(
    request: Request,
    file_path: str,
    response: Response,
) -> Response:
    """Delete a file.  
    NOTE: DELETE requests MUST NOT return a body in the response."""

    print(request.app.state)
    delete_s3_object(
        bucket_name=s3_bucket_name,
        object_key=file_path,
    )
    response.status_code = status.HTTP_204_NO_CONTENT

    return response

def create_app(s3_bucket_name: Optional[str] = None):
    s3_bucket_name = s3_bucket_name or os.environ["s3_bucket_name"]
    app = FastAPI()

    app.include_router(ROUTER)
    return app


    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
