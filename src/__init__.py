from utils.Lexer import Lexer
from utils.Execute import Exec
import sys


class Interpreter:

    def __init__(self, file_path: str):

        self._path = file_path
        if not self._validate_path():
            raise Exception("Invalid file type: .%s (allowed: .df)" % self._path.split("\\")[len(self._path.split("\\")) - 1].split(".")[1])
        with open(self._path, "r") as rFile:
            self._data = self._clean(rFile.readlines())
        self._data.remove("")
        self._lexer = Lexer(self._data)
        self._exec = Exec(self._lexer.get_lexed_stream())

    @staticmethod
    def _clean(raw_data: list):
        return "".join(i.replace("\n", "") for i in raw_data).split(";")

    def _validate_path(self):
        return self._path.split("\\")[len(self._path.split("\\")) - 1].split(".")[1] == "df"


if __name__ == "__main__":
    Interpreter(sys.argv[1])
    exit(-1)
