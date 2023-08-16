import re

IDENTIFIER = '[a-zA-Z0-9-]'
DOTSEP_ID = rf'{IDENTIFIER}+(\.{IDENTIFIER}+)*'
PRE_RELEASE = rf'({{}}{DOTSEP_ID})'
BUILD = rf'({{}}{DOTSEP_ID})'
VERSION_CORE = rf'({{}}\d+)\.({{}}\d+)\.({{}}\d+)'

GROUP_ID = f'?P<{{}}>'
SEMVAR_RAW = rf'[Vv]?({{}}{VERSION_CORE})(-{PRE_RELEASE})?(\+{BUILD})?'

SEMVAR = re.compile(r'{}$'.format(SEMVAR_RAW.format(GROUP_ID.format('version'),
                                                    GROUP_ID.format('major'),
                                                    GROUP_ID.format('minor'),
                                                    GROUP_ID.format('patch'),
                                                    GROUP_ID.format('pre_release'),
                                                    GROUP_ID.format('build'))))

args = ('',) * 6
SEMVAR_PLAIN = SEMVAR_RAW.format(*args)
DATE = r'(?P<date>(\d{4}-\d{2}-\d{2}))'
LINK = r'(?P<link>(\s*\(.*\)))'
DELIMITER = re.compile(rf'##\s+(?P<semvar>((\[{SEMVAR_PLAIN}]{LINK}?)|{SEMVAR_PLAIN}))\s+-\s+{DATE}')
