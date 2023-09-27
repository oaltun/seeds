from pathlib import Path
from typing import Optional
from schemas.DirFilelistGet import DirFilelistGet
from schemas.FileToWrite import FileToWrite
import pydantic
from pydantic import validator, Field

import instructor
from instructor import OpenAISchema

# instructor.patch() # Enables the response_model 

class AIRequests(OpenAISchema):
    "AI can ask system for information to understand its environment by file_to_read and dir_filelist_get. AI can also modify/rewrite using file_to_read."
    intent: str = Field("", description="AI's aim for this request", example="I want to see contents of the directory")
    file_to_read: Optional[str] = None
    file_to_write: Optional[FileToWrite] = None
    dir_filelist_get: Optional[DirFilelistGet] = None
