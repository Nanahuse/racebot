import contextlib
from typing import Generator


class Semaphore:
    def __init__(self):
        self._semaphores: set[int] = set()

    @contextlib.contextmanager
    def acquire(self, key: int) -> Generator[bool]:
        if key in self._semaphores:
            yield False
            return

        self._semaphores.add(key)
        try:
            yield True
        finally:
            self._semaphores.remove(key)
