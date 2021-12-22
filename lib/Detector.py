from .FileRepository import FileRepository
import requests


class Detector:
    def __init__(self, url, callback):
        self._target_url = url
        self._callback = callback
        self._repository = FileRepository('.previous')

    def tick(self):
        now = requests.get(self._target_url).text
        prev = self._repository.load()

        self._repository.save(now)

        if prev is None:
            return

        if now == prev:
            return

        self._callback(prev, now)
