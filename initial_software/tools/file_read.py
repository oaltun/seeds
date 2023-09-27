from pathlib import Path
from schemas.FileToWrite import FileToWrite


def file_read(obj:str):
    return Path(obj).read_text()
