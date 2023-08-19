import re

from ._pattern import DELIMITER, LINK, CHANGE
from .version import Unreleased, SemanticVersion


__all__ = ['ChangelogFormatException', 'Changes', 'Changelog']


class ChangelogFormatException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


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


class Changelog:
    __slots__ = '_links', '_versions', '_changes'

    def __init__(self, changelog: str):
        with open(changelog, 'r') as f:
            contents = f.readlines()

        self._versions = []
        self._links = {}
        self._changes = {}
        self._parseChangelog(contents)

    def _checkLink(self, line):
        match = LINK.match(line)
        if match:
            groups = match.groupdict()
            if groups['unreleased']:
                self._links[Unreleased] = groups['url']
                return 1
            elif groups['version']:
                self._links[SemanticVersion(groups['version'])] = groups['url']
                return 1
        return 0

    def _addVersion(self, match: re.Match):
        groups = match.groupdict()
        version = SemanticVersion(groups['unreleased'] or groups['version'])
        self._versions.append(version)
        if groups['url']:
            self._links[version] = groups['url']

        return version

    def _parseChangelog(self, contents: list[str]):
        body = contents
        firstVersion = None
        for i, line in enumerate(contents):
            if self._checkLink(line):
                continue
            match = DELIMITER.match(line)
            if match:
                firstVersion = self._addVersion(match)
                body = contents[i+1:]
                break

        if firstVersion is None:
            raise ChangelogFormatException('no versions found in changelog')
        currentVersion = firstVersion

        changes = ''
        for line in body:
            if match := DELIMITER.match(line):
                self._changes[currentVersion] = Changes(changes.strip())
                currentVersion = self._addVersion(match)
                changes = ''
            elif self._checkLink(line):
                continue
            else:
                changes += line

        self._changes[currentVersion] = Changes(changes.strip())

    @property
    def versions(self) -> list[SemanticVersion]:
        return self._versions

    @property
    def changes(self) -> dict[SemanticVersion, Changes]:
        return self._changes

    @property
    def links(self) -> dict[SemanticVersion, str]:
        return self._links

    def __getitem__(self, item: str | SemanticVersion) -> Changes:
        if isinstance(item, str):
            item = SemanticVersion(item)
        if isinstance(item, SemanticVersion):
            return self._changes[item]

        raise TypeError('item must be a str or SemanticVersion type')

    def __contains__(self, item: str | SemanticVersion):
        if isinstance(item, str):
            item = SemanticVersion(item)
        if isinstance(item, SemanticVersion):
            return item in self._versions

        raise TypeError('item must be a str or SemanticVersion type')

    def getVersion(self, version: str | SemanticVersion) -> dict:
        if isinstance(version, str):
            version = SemanticVersion(version)
        if not isinstance(version, SemanticVersion):
            raise TypeError('version must be a str or SemanticVersion type')

        if version not in self._versions:
            raise ValueError(f'version ({version}) not found in changelog')

        return {'version': version.toDict(), 'link': self._links.get(version) or '',
                'changes': self._changes.get(version).toDict()}

    def toDict(self) -> dict:
        rtn = {}
        for version in self._versions:
            rtn[str(version)] = self.getVersion(version)

        return rtn
