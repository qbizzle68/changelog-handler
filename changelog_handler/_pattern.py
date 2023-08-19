import re

IDENTIFIER = '[a-zA-Z0-9-]'
DOTSEP_ID = rf'{IDENTIFIER}+(?:\.{IDENTIFIER}+)*'
PRE_RELEASE = rf'(?P<pre_release>{DOTSEP_ID})'
BUILD = rf'(?P<build>{DOTSEP_ID})'
VERSION_CORE = rf'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'

SEMVAR_RAW = rf'[Vv]?(?P<version>{VERSION_CORE}(?:-{PRE_RELEASE})?(?:\+{BUILD})?)'

SEMVAR = re.compile(f'{SEMVAR_RAW}$')
DATE = r'(?P<date>\d{4}-\d{2}-\d{2})'
URL = r'\s*\((?P<url>.+)\)'
# DELIMITER = re.compile(rf'##\s+(\[)?(?:(?P<unreleased>[Uu]nreleased)|{SEMVAR_RAW})(?(1)])(?:{URL})?\s+-\s+{DATE}')
DELIMITER = re.compile(rf'##\s+(\[)?(?:(?P<unreleased>[Uu]nreleased)|{SEMVAR_RAW})(?(1)])(?:{URL})?(?(3)\s+-\s+{DATE}|)')

LINK = re.compile(rf'\[(?:(?P<unreleased>[Uu]nreleased)|{SEMVAR_RAW})]:\s+(?P<url>.+)')

# regex for change tags
TAGS = 'added|changed|deprecated|removed|fixed|security'
CHANGE = rf'(?P<tag_literal>###\s+(?P<tag_name>{TAGS}).*?\n)(?P<content>.*?\n*)(?=##+|$)'
