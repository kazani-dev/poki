import re
from hashlib import sha256
from pathlib import Path


HEX_REGEX = re.compile(r"^[a-zA-Z0-9]+$")


class PasteStore:
    def __init__(self, data_directory: Path) -> None:
        self.data_directory = data_directory

        if not self.data_directory.exists():
            self.data_directory.mkdir(parents=True)

    def add(self, data: bytes) -> str:
        hash = sha256(data, usedforsecurity=False).hexdigest()
        directory = self.data_directory / hash[0:2] / hash[2:4]

        if not directory.exists():
            directory.mkdir(parents=True)

        file = directory / hash

        if not file.exists():
            file.write_bytes(data)

        return hash

    def get(self, hash: str) -> bytes | None:
        hash = hash.strip().lower()

        if not HEX_REGEX.match(hash):
            # Not a hash.
            return None

        file = self.data_directory / hash[0:2] / hash[2:4] / hash

        if not file.exists():
            return None

        return file.read_bytes()

    def remove(self, hash: str) -> None:
        hash = hash.strip().lower()

        if not HEX_REGEX.match(hash):
            # Not a hash.
            return None

        file = self.data_directory / hash[0:2] / hash[2:4] / hash

        if not file.exists():
            return None

        file.unlink()

        if len(list(file.parent.iterdir())) == 0:
            file.parent.rmdir()

        if len(list(file.parent.parent.iterdir())) == 0:
            file.parent.parent.rmdir()
