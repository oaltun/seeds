from pathlib import Path

from schemas.DirFilelistGet import DirFilelistGet

def dir_filelist_get(self:DirFilelistGet):

    list = []

    for path in Path(self.directory).rglob(self.pattern):
        bad_path=False
        for exclude in self.excludes:
            if exclude in path.as_posix():
                bad_path=True
        if not bad_path:
            list.append(path)
    return list
