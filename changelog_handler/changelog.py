import re

from ._pattern import DELIMITER, LINK, CHANGE
from .version import Unreleased, SemanticVersion


class Changes:
    __slots__ = '_added', '_changed', '_deprecated', '_removed', '_fixed', '_security'

    def __init__(self, contents: str):
        if not isinstance(contents, str):
            raise TypeError('contents must be a str type')

        self._added = {}
        self._changed = {}
        self._deprecated = {}
        self._removed = {}
        self._fixed = {}
        self._security = {}

        self._parseTags(contents)

    def _parseTags(self, contents):
        while contents:
            match = re.match(CHANGE, contents, re.IGNORECASE | re.DOTALL)
            if not match:
                raise ValueError('unable to parse version changes')
            if re.match(f'{match[2]}', 'added', re.IGNORECASE):
                self._added = {'tag_raw': match[1], 'content': match[3]}
            elif re.match(f'{match[2]}', 'changed', re.IGNORECASE):
                self._changed = {'tag_raw': match[1], 'content': match[3]}
            elif re.match(f'{match[2]}', 'deprecated', re.IGNORECASE):
                self._deprecated = {'tag_raw': match[1], 'content': match[3]}
            elif re.match(f'{match[2]}', 'removed', re.IGNORECASE):
                self._removed = {'tag_raw': match[1], 'content': match[3]}
            elif re.match(f'{match[2]}', 'fixed', re.IGNORECASE):
                self._fixed = {'tag_raw': match[1], 'content': match[3]}
            elif re.match(f'{match[2]}', 'security', re.IGNORECASE):
                self._security = {'tag_raw': match[1], 'content': match[3]}
            contents = contents.replace(match[0], '')

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        singleString = ''
        for d in (self._added, self._changed, self._deprecated, self._removed, self._fixed, self._security):
            singleString += f"{d.get('tag_raw', '')}{d.get('content', '')}"
        return f'Changes({singleString})'

    @property
    def added(self) -> dict:
        return self._added

    @property
    def changed(self) -> dict:
        return self._changed

    @property
    def deprecated(self) -> dict:
        return self._deprecated

    @property
    def removed(self) -> dict:
        return self._removed

    @property
    def fixed(self) -> dict:
        return self._fixed

    @property
    def security(self) -> dict:
        return self._security

    def toDict(self) -> dict:
        return {'added': self._added, 'changed': self._changed, 'deprecated': self._deprecated,
                'removed': self._removed, 'fixed': self._fixed, 'security': self._security}

