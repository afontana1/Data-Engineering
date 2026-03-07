import gzip
from abc import ABC, abstractmethod, abstractproperty
from builtins import str
from pathlib import Path
from sys import getsizeof

ENCODING_TYPE = 'utf-8'


class Data:
    """Data Class
    Stores data in string or bytes. 
    Always returns bytes
    """

    # decrease memory usage from 48 to 40 bytes
    __slots__ = ('_data')

    def __init__(self, data: str | bytes) -> None:
        self._data = data

    def _get_str(self) -> str:
        """Get string from stored data and convert using the set encoding"""
        if type(self._data) is not str:
            return str(self._data, encoding=ENCODING_TYPE)  # type: ignore
        return self._data

    def _get_bytes(self) -> bytes:
        """Get bytes from stored data and convert using the set encoding"""
        if type(self._data) is not bytes:
            return bytes(self._data, encoding=ENCODING_TYPE)  # type: ignore
        return self._data

    @property
    def text(self) -> str:
        return self._get_str()

    @text.setter
    def text(self, value: str | bytes) -> None:
        self._data = value

    @property
    def blob(self) -> bytes:
        return self._get_bytes()

    @blob.setter
    def blob(self, value: str | bytes) -> None:
        self._data = value

    @property
    def size(self) -> int:
        return getsizeof(self._data)


class File:
    """File Class
    Overwrites strings or bytes to a file
    Closes and opens file on every read/write
    """

    __slots__ = ('_path', '_file', '_data')

    def __init__(self, path: str, create: bool = True) -> None:
        self._path: Path = Path(path)
        if not self._path.is_file():
            match create:
                case True:
                    self._path.touch()
                case False:
                    raise OSError(f'File with path "path" does not exist')

    def _open(self) -> None:
        self._file = self._path.open(mode='r+', encoding=ENCODING_TYPE)

    def _close(self) -> None:
        self._file.close()

    @property
    def data(self) -> Data:
        self._open()
        self._data = Data(self._file.read())
        self._close()
        return self._data

    def write(self, content: Data) -> None:
        if type(content) is not Data:
            raise TypeError('Content must be a Data type')
        self._data = content
        self._open()
        self._file.write(self._data.text)
        self._file.truncate()
        self._close()

    @property
    def size(self) -> int:
        return self._data.size


class DataSourceDecorator(ABC):
    """Abstract Data Source Decorator"""

    @abstractmethod
    def __init__(self, data: Data) -> None:
        self._data = data

    @abstractmethod
    def _compress(self, blob: bytes) -> None:
        ...

    @abstractmethod
    def _inflate(self, blob: bytes) -> None:
        ...

    def read(self) -> Data:
        return self._data


class GZIPDecorator(DataSourceDecorator):
    """GZIP Compression Decorator"""

    def __init__(self, data: Data | File, compressed: bool = False, compresslevel: int = 9) -> None:
        if type(data) is Data:
            blob = data.blob
        elif type(data) is File:
            blob = data.data.blob
        else:
            raise TypeError(f'Unsupported type "{type(data)}"')

        self._compresslevel = compresslevel

        if compressed:
            self._inflate(blob)
        else:
            self._compress(blob)

    def _compress(self, blob: bytes):
        self._data = Data(gzip.compress(blob, self._compresslevel))
        before, after = getsizeof(blob), self._data.size
        print(f'Compressed {before}B to {after}B ({before / after:.2f}x)')

    def _inflate(self, blob: bytes):
        self._data = Data(gzip.decompress(blob))
        before, after = getsizeof(blob), self._data.size
        print(f'Decompressed {before}B to {after}B ({before / after:.2f}x)')
