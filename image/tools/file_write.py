from pathlib import Path
from schemas.FileToWrite import FileToWrite


def file_write(obj:FileToWrite):
    Path(obj.path).write_text(obj.content)
    return True # success