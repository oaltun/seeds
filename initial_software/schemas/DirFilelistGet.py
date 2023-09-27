from pydantic import BaseModel, Field, validator
from typing import Optional, List

class DirFilelistGet(BaseModel):
    directory: Optional[str] = Field(default=".", description="The directory to search in")
    pattern: Optional[str] = Field(default="*", description="The pattern to search for")
    excludes: Optional[List[str]] = Field(default=['/__pycache__/', '/.git/', 'venv', '.env', '/.condaenv/', '/env/'], description="List of excluded directories")

    @validator("directory")
    def validate_directory(cls, value):
        allowed_prefixes = ["/app/env1", "/app/env2"]
        if not any(value.startswith(prefix) for prefix in allowed_prefixes):
            raise ValueError("Directory must be within /app/env1 or /app/env2")
        return value
