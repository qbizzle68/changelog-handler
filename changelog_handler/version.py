import re
from functools import total_ordering
from changelog_handler._pattern import SEMVAR

__all__ = ['SemanticVersion', 'InvalidSemanticVersion', 'Unreleased']


class InvalidSemanticVersion(Exception):
    def __init__(self, *args):
        super().__init__(*args)


@total_ordering
class SemanticVersion:
    __slots__ = '_major', '_minor', '_patch', '_preRelease', '_build'

    def __new__(cls, version: str):
        if not isinstance(version, str):
            raise TypeError('version must be a str type')

        if re.fullmatch('unreleased', version, re.IGNORECASE):
            return Unreleased

        self = object.__new__(cls)

        match = SEMVAR.fullmatch(version)
        if match is None:
            raise InvalidSemanticVersion('version string does not contain a valid sematic version')

        results = match.groupdict(default='')
        self._major = int(results['major'])
        self._minor = int(results['minor'])
        self._patch = int(results['patch'])
        self._preRelease = results['pre_release']
        self._build = results['build']
        for p in self._preRelease.split('.'):
            if p and p != '0' and p[0] == '0':
                raise InvalidSemanticVersion('pre-release dot separated identifiers must not include leading zeros')

        return self

    def __str__(self) -> str:
        rtn = f'{self._major}.{self._minor}.{self._patch}'
        if self._preRelease:
            rtn += f'-{self._preRelease}'
        if self._build:
            rtn += f'+{self._build}'

        return rtn

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.__str__()}")'

    def __hash__(self):
        return hash((self._major, self._minor, self._patch, self._preRelease, self._build))

    def __reduce__(self):
        return self.__class__, (self.__str__(),)

    @property
    def version(self):
        return f'{self._major}.{self._minor}.{self._patch}'

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def preRelease(self):
        return self._preRelease

    @property
    def buildMetadata(self):
        return self._build

    def __eq__(self, other: 'SemanticVersion') -> bool:
        if isinstance(other, SemanticVersion):
            return (self._major == other._major and self._minor == other._minor and self._patch == other._patch
                    and self._preRelease == other._preRelease)

        return NotImplemented

    def _compareVersion(self, rhs: 'SemanticVersion') -> int:
        """Compare self to rhs with version numbering only. Returns -1 if self < rhs, 1 if self > rhs, 0 if they are
        equal."""

        if self._major < rhs._major:
            return -1
        elif self._major > rhs._major:
            return 1

        if self._minor < rhs._minor:
            return -1
        elif self._minor > rhs._minor:
            return 1

        if self._patch < rhs._patch:
            return -1
        elif self._patch > rhs._patch:
            return 1

        return 0

    @staticmethod
    def _compareToInt(lhs, rhs):
        if lhs < rhs:
            return -1
        elif lhs > rhs:
            return 1
        return 0

    @staticmethod
    def _compareIdentifiers(rId: str, lId: str):
        if rId.isdigit():
            rId = int(rId)
            if lId.isdigit():
                lId = int(lId)
                return SemanticVersion._compareToInt(rId, lId)
            else:
                return -1
        elif lId.isdigit():
            return 1
        return SemanticVersion._compareToInt(rId, lId)

    def _comparePreRelease(self, rhs: 'SemanticVersion') -> int:
        if self._preRelease and not rhs._preRelease:
            return -1
        elif not self._preRelease and rhs._preRelease:
            return 1
        elif self._preRelease == rhs._preRelease:
            return 0

        rhsIdentifiers = self._preRelease.split('.')
        lhsIdentifiers = rhs._preRelease.split('.')

        for rId, lId in zip(rhsIdentifiers, lhsIdentifiers):
            result = self._compareIdentifiers(rId, lId)
            if result != 0:
                return result

        if len(rhsIdentifiers) < len(lhsIdentifiers):
            return -1
        elif len(rhsIdentifiers) > len(lhsIdentifiers):
            return 0

    def __lt__(self, other: 'SemanticVersion') -> bool:
        if isinstance(other, SemanticVersion):
            cmpVersion = self._compareVersion(other)
            if cmpVersion == -1:
                return True
            elif cmpVersion == 1:
                return False

            cmpPre = self._comparePreRelease(other)
            if cmpPre == -1:
                return True
            return False

        return NotImplemented

    def toDict(self):
        """Return a dict with all parts of a semantic version."""
        return {'major': self._major, 'minor': self._minor, 'patch': self._patch,
                'pre_release': self._preRelease, 'build_metadata': self._build}


class UnreleasedType(SemanticVersion):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __str__(self):
        return 'Unreleased'

    def __repr__(self):
        return 'Unreleased'

    def __hash__(self):
        return hash('unreleased')

    def __eq__(self, other: SemanticVersion):
        if type(other) == SemanticVersion:
            return False
        elif other is Unreleased:
            return True

        return NotImplemented

    def __lt__(self, other: SemanticVersion):
        if type(other) == SemanticVersion:
            return False
        elif other is Unreleased:
            return False

        return NotImplemented

    def toDict(self) -> dict:
        return {}


Unreleased = UnreleasedType()
