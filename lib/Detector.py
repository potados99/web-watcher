from .FileRepository import FileRepository
import requests


class Detector:
    def __init__(self, url, callback):
        self._target_url = url
        self._callback = callback
        self._repository = FileRepository('.previous')

    def tick(self):
        fetched = requests.get(self._target_url).text
        stored = self._repository.load()

        self._repository.save(fetched)

        if stored is None:
            return

        if fetched == stored:
            return

        self._callback()
