class FileRepository:
    def __init__(self, file_name):
        self._file_name = file_name

    def save(self, content):
        with open(self._file_name, 'w') as f:
            f.write(content)

    def load(self):
        try:
            with open(self._file_name, 'r') as f:
                return f.read()
        except (FileNotFoundError, ValueError, SyntaxError):
            return None
