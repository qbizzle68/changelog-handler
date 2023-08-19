import re
import unittest

from changelog_handler._pattern import PRE_RELEASE, BUILD, VERSION_CORE, SEMVAR, DATE, URL, DELIMITER, LINK, TAGS, \
    CHANGE

testStrings = {
    'preValidTests': [
        '1',
        'alpha',
        'alpha.beta',
        'alpha.3',
    ],
    'preInvalidTests': [
        'alpha+beta',
        'alpha.beta..2',
        'alpha.beta#',
        # this needs to be worked out in the regex
        # 'alpha.023',
    ],
    'buildValidTests': [
        '1',
        'alpha',
        'alpha.beta',
        'sha.1e4c5d2a',
        'sha.8F3E8CA2',
        '1234.5421.523',
        'b--3421',
    ],
    'buildInvalidTests': [
        'build..12343',
        'b--3853?',
    ],
    'versionCoreValidTests': [
        '1.0.0',
        '1.2.3',
        '4.5.6',
        '7.8.9',
        '12.0.0',
        '0.23.0',
        '0.0.34',
        '45.56.0',
        '67.0.78',
        '0.89.90',
        '12.34.56',
    ],
    'versionCoreInvalidTests': [
        '1.0',
        '1.0.a',
        '1.b.3',
        '-.2.3',
    ],
    'semvarValidTests': [
        '1.0.0',
        'v1.0.0',
        'V1.0.0',
        '2.3.4-alpha',
        'v2.3.4-alpha',
        'V2.3.4-alpha',
        '3.4.5-alpha+1234',
        'v3.4.5-alpha+1234',
        'V3.4.5-alpha+1234',
        '1.2.3-alpha.beta.2+exp.sha--1234',
    ],
    'semvarInvalidTests': [
        'alpha+beta',
        'alpha.beta..2',
        'alpha.beta#',
        # this needs to be worked out in the regex
        # 'alpha.023',
        'build..12343',
        'b--3853?',
        '1.0',
        '1.0.a',
        '1.b.3',
        '-.2.3',
        '1.2.3-alpha+1234 blah',
    ],
    'dateValidTests': [
        '2023-08-16',
        '1999-12-31',
        '9999-99-99',
    ],
    'dateInvalidTests': [
        '12-23-1970',
        '00-00-00',
    ],
    'urlValidTests': [
        '(www.google.com)',
        '(google.com)',
        '(aijfqejnvsiefhsl2345)',
        ' (github.com)',
        '   (pypi.org)',
    ],
    'urlInvalidTests': [
        'google.com',
        '()',
    ],
    'delimiterValidTests': [
        '## [1.2.3] - 2023-08-16',
        '## [1.2.3]  - 2023-08-16',
        '## [1.2.3]  -  2023-08-16',
        '## 1.2.3 - 2023-08-16',
        '## 1.2.3  - 2023-08-16',
        '## 1.2.3  -  2023-08-16',
        '## [1.2.3](example.com) - 2023-08-16',
        '## [1.2.3](example.com)  - 2023-08-16',
        '## [1.2.3](example.com)  -  2023-08-16',
        '## [unreleased] - 2023-08-16',
        '## [Unreleased] - 2023-08-16',
        '## [Unreleased](example.com) - 2023-08-16',
        '##  [1.2.3] - 2023-08-16',
    ],
    'delimiterInvalidTests': [
        '## 1.2.3] - 2023-08-16',
        '## [1.2.3]- 2023-08-16',
        '## [1.2.3] -2023-08-16',
        '### [1.2.3] - 2023-08-16',
        '[1.2.3] - 2023-08-16',
    ],
    'linkValidTests': [
        '[1.2.3]: https://github.com',
        '[1.0.0]: google.com',
        '[Unreleased]: blahblahblah',
        '[unreleased]: example.com',
    ],
    'linkInvalidTests': [
        '1.2.3: example.com',
        '[1.2.3] example.com',
        '[1.2.3]:example.com',
    ],
    'tagsTests': [
        'added',
        'Added',
        'ADDED',
        'changed',
        'Changed',
        'CHANGED',
        'deprecated',
        'Deprecated',
        'DEPRECATED',
        'removed',
        'Removed',
        'REMOVED',
        'fixed',
        'Fixed',
        'FIXED',
        'security',
        'Security',
        'SECURITY',
    ],
    'changeValidTests': [
        '''### Added

- Arabic translation (#444).
- v1.1 French translation.
- v1.1 Dutch translation (#371).
- v1.1 Russian translation (#410).
- v1.1 Japanese translation (#363).
- v1.1 Norwegian Bokmål translation (#383).
- v1.1 "Inconsistent Changes" Turkish translation (#347).
- Default to most recent versions available for each languages
- Display count of available translations (26 to date!)
- Centralize all links into `/data/links.json` so they can be updated easily

### Fixed''',
        '''### Fixed

- Improve French translation (#377).
- Improve id-ID translation (#416).
- Improve Persian translation (#457).
- Improve Russian translation (#408).
- Improve Swedish title (#419).
- Improve zh-CN translation (#359).
- Improve French translation (#357).
- Improve zh-TW translation (#360, #355).
- Improve Spanish (es-ES) transltion (#362).
- Foldout menu in Dutch translation (#371).
- Missing periods at the end of each change (#451).
- Fix missing logo in 1.1 pages
- Display notice when translation isn't for most recent version
- Various broken links, page versions, and indentations.''',
        '''### Added extra chars

- Explanation of the recommended reverse chronological release ordering.

''',
        '''### Added

- "Why should I care?" section mentioning The Changelog podcast.

[link]: google.com

'''
    ]
}


class PatternTest(unittest.TestCase):

    def testPreReleaseRegex(self):
        for test in testStrings['preValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.fullmatch(PRE_RELEASE, test))
        for test in testStrings['preInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(re.fullmatch(PRE_RELEASE, test))

    def testPreReleaseGroups(self):
        for test in testStrings['preValidTests']:
            with self.subTest():
                match = re.fullmatch(PRE_RELEASE, test)
                self.assertTrue(all(match.groups()))

    def testBuildRegex(self):
        for test in testStrings['buildValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.fullmatch(BUILD, test))
        for test in testStrings['buildInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(re.fullmatch(BUILD, test))

    def testBuildGroups(self):
        for test in testStrings['buildValidTests']:
            with self.subTest(msg=test):
                match = re.fullmatch(BUILD, test)
                self.assertTrue(all(match.groups()))

    def testVersionCoreRegex(self):
        for test in testStrings['versionCoreValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.fullmatch(VERSION_CORE, test))
        for test in testStrings['versionCoreInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(re.fullmatch(VERSION_CORE, test))

    def testVersionCoreGroups(self):
        answers = [
            ('1', '0', '0'),
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
            ('12', '0', '0'),
            ('0', '23', '0'),
            ('0', '0', '34'),
            ('45', '56', '0'),
            ('67', '0', '78'),
            ('0', '89', '90'),
            ('12', '34', '56'),
        ]

        for test, answer in zip(testStrings['versionCoreValidTests'], answers):
            with self.subTest(msg=test):
                match = re.fullmatch(VERSION_CORE, test)
                self.assertTrue(all(match.groups()))
                groups = match.groupdict()
                ansDict = {'major': answer[0], 'minor': answer[1], 'patch': answer[2]}
                self.assertEqual(groups, ansDict)

    def testSemVarRegex(self):
        for test in testStrings['semvarValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(SEMVAR.match(test))
        for test in testStrings['semvarInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(SEMVAR.match(test))

    def testSemVarGroups(self):
        answers = [
            ('1.0.0', '1', '0', '0', '', ''),
            ('1.0.0', '1', '0', '0', '', ''),
            ('1.0.0', '1', '0', '0', '', ''),
            ('2.3.4-alpha', '2', '3', '4', 'alpha', ''),
            ('2.3.4-alpha', '2', '3', '4', 'alpha', ''),
            ('2.3.4-alpha', '2', '3', '4', 'alpha', ''),
            ('3.4.5-alpha+1234', '3', '4', '5', 'alpha', '1234'),
            ('3.4.5-alpha+1234', '3', '4', '5', 'alpha', '1234'),
            ('3.4.5-alpha+1234', '3', '4', '5', 'alpha', '1234'),
            ('1.2.3-alpha.beta.2+exp.sha--1234', '1', '2', '3', 'alpha.beta.2', 'exp.sha--1234')
        ]

        for test, answer in zip(testStrings['semvarValidTests'], answers):
            with self.subTest(msg=test):
                match = SEMVAR.match(test)
                ansDict = {'version': answer[0], 'major': answer[1], 'minor': answer[2],
                           'patch': answer[3], 'pre_release': answer[4], 'build': answer[5]}
                self.assertEqual(match.groupdict(default=''), ansDict)

    def testDateRegex(self):
        for test in testStrings['dateValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.fullmatch(DATE, test))
        for test in testStrings['dateInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(re.fullmatch(DATE, test))

    def testDateGroups(self):
        answers = ('2023-08-16', '1999-12-31', '9999-99-99')
        for test, answer in zip(testStrings['dateValidTests'], answers):
            with self.subTest(msg=test):
                self.assertEqual(re.fullmatch(DATE, test)[1], answer)

    def testUrlRegex(self):
        for test in testStrings['urlValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.fullmatch(URL, test))
        for test in testStrings['urlInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(re.fullmatch(URL, test))

    def testUrlGroups(self):
        answers = ('www.google.com', 'google.com', 'aijfqejnvsiefhsl2345',
                   'github.com', 'pypi.org',)

        for test, answer in zip(testStrings['urlValidTests'], answers):
            with self.subTest(msg=test):
                self.assertEqual(re.fullmatch(URL, test)[1], answer)

    def testDelimiterRegex(self):
        for test in testStrings['delimiterValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(DELIMITER.match(test))
        for test in testStrings['delimiterInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(DELIMITER.match(test))

    def testDelimiterGroups(self):
        answers = [
            ('[', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', 'example.com', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', 'example.com', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', 'example.com', '2023-08-16'),
            ('[', 'unreleased', '', '', '', '', '', '', '', '2023-08-16'),
            ('[', 'Unreleased', '', '', '', '', '', '', '', '2023-08-16'),
            ('[', 'Unreleased', '', '', '', '', '', '', 'example.com', '2023-08-16'),
            ('[', '', '1.2.3', '1', '2', '3', '', '', '', '2023-08-16'),
        ]

        for test, answer in zip(testStrings['delimiterValidTests'], answers):
            with self.subTest(msg=test):
                match = DELIMITER.match(test)
                self.assertEqual(match.groups(default=''), answer)

    def testLinkRegex(self):
        for test in testStrings['linkValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(LINK.match(test))
        for test in testStrings['linkInvalidTests']:
            with self.subTest(msg=test):
                self.assertFalse(LINK.match(test))

    def testLinkGroups(self):
        answers = [
            ('', '1.2.3', '1', '2', '3', '', '', 'https://github.com'),
            ('', '1.0.0', '1', '0', '0', '', '', 'google.com'),
            ('Unreleased', '', '', '', '', '', '', 'blahblahblah'),
            ('unreleased', '', '', '', '', '', '', 'example.com'),
        ]

        for test, answer in zip(testStrings['linkValidTests'], answers):
            with self.subTest(msg=test):
                match = LINK.match(test)
                self.assertEqual(match.groups(default=''), answer)

    def testTagsRegex(self):
        for test in testStrings['tagsTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.match(TAGS, test, re.I))

    def testChangeRegex(self):
        for test in testStrings['changeValidTests']:
            with self.subTest(msg=test):
                self.assertTrue(re.match(CHANGE, test, re.I | re.DOTALL))

    def testChangeGroups(self):
        answers = [
            ('''### Added
''', 'Added', '''
- Arabic translation (#444).
- v1.1 French translation.
- v1.1 Dutch translation (#371).
- v1.1 Russian translation (#410).
- v1.1 Japanese translation (#363).
- v1.1 Norwegian Bokmål translation (#383).
- v1.1 "Inconsistent Changes" Turkish translation (#347).
- Default to most recent versions available for each languages
- Display count of available translations (26 to date!)
- Centralize all links into `/data/links.json` so they can be updated easily

'''),
            ('''### Fixed
''', 'Fixed', '''
- Improve French translation (#377).
- Improve id-ID translation (#416).
- Improve Persian translation (#457).
- Improve Russian translation (#408).
- Improve Swedish title (#419).
- Improve zh-CN translation (#359).
- Improve French translation (#357).
- Improve zh-TW translation (#360, #355).
- Improve Spanish (es-ES) transltion (#362).
- Foldout menu in Dutch translation (#371).
- Missing periods at the end of each change (#451).
- Fix missing logo in 1.1 pages
- Display notice when translation isn't for most recent version
- Various broken links, page versions, and indentations.'''),
            ('''### Added extra chars
''', 'Added', '''
- Explanation of the recommended reverse chronological release ordering.

'''),
            ('''### Added
''', 'Added', '''
- "Why should I care?" section mentioning The Changelog podcast.

[link]: google.com

''')
        ]
        for test, answer in zip(testStrings['changeValidTests'], answers):
            with self.subTest(msg=test):
                self.assertEqual(re.match(CHANGE, test, re.I | re.DOTALL).groups(), answer)
