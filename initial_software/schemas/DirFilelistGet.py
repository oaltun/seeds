from pathlib import Path
from typing import List, Optional
import pydantic
from pydantic import validator

import instructor
from instructor import OpenAISchema

# instructor.patch() # Enables the response_model 

class DirFilelistGet(OpenAISchema):
    "Data for creating a recursive directory listing like 'find' in linux."
    directory: Optional[str] = "."
    pattern: Optional[str] = '*'
    excludes: Optional[List[str]] = ['/__pycache__/','/.git/',]