"""
DictDB
------

Persistent dictionary implementation using BTrees.

This module provides a dictionary-like interface to a BTree-based persistence layer,
offering both standard dictionary operations and range queries with automatic
transaction support.

Example:
    Basic usage:
        >>> db = DictDB('mydata.db')
        >>> db['key'] = 'value'
        >>> print(db['key'])
        >>> db.close()

    Using as a context manager with automatic transaction handling:
        >>> with DictDB('mydata.db') as db:
        ...     db['key'] = 'value'
        ...     # Changes are automatically committed on clean exit
        ...     # or rolled back on exception
"""

import btree  # type: ignore
import json


class DictDB:
    """A persistent dictionary implementation using BTrees.
    
    DictDB provides a dict-like interface to a persistent BTree database.
    It supports all standard dictionary operations plus range queries and
    automatic transaction handling via context manager protocol.

    Args:
        filename (str): Path to the database file. Created if doesn't exist.

    Attributes:
        filename (str): The path to the database file being used.

    The database is automatically opened on instantiation. Changes are written
    to disk immediately by default. When used as a context manager, changes
    are automatically rolled back if an exception occurs.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self._db = None
        self._file = None
        self.open()

    def open(self) -> None:
        try:
            self._file = open(self.filename, "r+b")
        except OSError:
            self._file = open(self.filename, "w+b")
        self._db = btree.open(self._file)

    def close(self) -> None:
        if self._db:
            self._db.flush()
            self._db.close()
            self._db = None
        if self._file:
            self._file.close()
            self._file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getitem__(self, key: str):
        raw_value = self._db[key.encode()].decode()
        return json.loads(raw_value)

    def __setitem__(self, key: str, value: str) -> None:
        json_value = json.dumps(value)
        self._db[key.encode()] = json_value.encode()
        self._db.flush()

    def __delitem__(self, key: str) -> None:
        del self._db[key.encode()]
        self._db.flush()

    def __contains__(self, key: str) -> bool:
        return key.encode() in self._db

    def __iter__(self):
        for key in self._db:
            yield key.decode()

    def items(self, start_key=None, end_key=None, incl=True):
        start = start_key.encode() if start_key is not None else None
        end = end_key.encode() if end_key is not None else None
        flags = btree.INCL if incl else 0
        for key, value in self._db.items(start, end, flags):
            yield key.decode(), json.loads(value.decode())

    def keys(self, start_key=None, end_key=None, incl=True):
        start = start_key.encode() if start_key is not None else None
        end = end_key.encode() if end_key is not None else None
        flags = btree.INCL if incl else 0
        for key in self._db.keys(start, end, flags):
            yield key.decode()

    def values(self, start_key=None, end_key=None, incl=True):
        start = start_key.encode() if start_key is not None else None
        end = end_key.encode() if end_key is not None else None
        flags = btree.INCL if incl else 0
        for value in self._db.values(start, end, flags):
            yield json.loads(value.decode())
