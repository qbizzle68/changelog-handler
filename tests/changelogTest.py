import pathlib
import unittest

from changelog_handler import Changelog, SemanticVersion, Unreleased


class ChangelogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        thisDir = pathlib.Path(__file__).parent
        cls.log = Changelog(thisDir / 'testlog.md')

    def testUnreleased(self):
        versionChanges = self.log['Unreleased']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[Unreleased])

        answers = [
            "\n- This is where I'd describe what's been added.",
            '',
            '',
            '',
            '',
            '',
        ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion111(self):
        # test access
        versionChanges = self.log['1.1.1']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('1.1.1')])

        answers = [
            '\n- Arabic translation (#444).\n- v1.1 French translation.\n- v1.1 Dutch translation (#371).\n- v1.1 '
            'Russian translation (#410).\n- v1.1 Japanese translation (#363).\n- v1.1 Norwegian BokmÃ¥l translation '
            '(#383).\n- v1.1 "Inconsistent Changes" Turkish translation (#347).\n- Default to most recent versions '
            'available for each languages\n- Display count of available translations (26 to date!)\n- Centralize all '
            'links into `/data/links.json` so they can be updated easily\n\n',
            '\n- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.\n\n',
            '',
            '\n- Unused normalize.css file\n- Identical links assigned in each translation file\n- Duplicate index file'
            ' for the english version',
            "\n- Improve French translation (#377).\n- Improve id-ID translation (#416).\n- Improve Persian translation"
            " (#457).\n- Improve Russian translation (#408).\n- Improve Swedish title (#419).\n- Improve zh-CN "
            "translation (#359).\n- Improve French translation (#357).\n- Improve zh-TW translation (#360, #355).\n- "
            "Improve Spanish (es-ES) transltion (#362).\n- Foldout menu in Dutch translation (#371).\n- Missing periods"
            " at the end of each change (#451).\n- Fix missing logo in 1.1 pages\n- Display notice when translation "
            "isn't for most recent version\n- Various broken links, page versions, and indentations.\n\n",
            ''
        ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion110(self):
        versionChanges = self.log['1.1.0']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('1.1.0')])

        answers = [
            '\n- Danish translation (#297).\n- Georgian translation from (#337).\n- Changelog inconsistency section in '
            'Bad Practices.\n\n',
            '',
            '',
            '',
            '\n- Italian translation (#332).\n- Indonesian translation (#336).',
            ''
        ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion100(self):
        versionChanges = self.log['1.0.0']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('1.0.0')])

        answers = [
            '\n- New visual identity by [@tylerfortune8](https://github.com/tylerfortune8).\n- Version navigation.\n- '
            'Links to latest released version in previous versions.\n- "Why keep a changelog?" section.\n- "Who needs a'
            ' changelog?" section.\n- "How do I make a changelog?" section.\n- "Frequently Asked Questions" section.\n-'
            ' New "Guiding Principles" sub-section to "How do I make a changelog?".\n- Simplified and Traditional '
            'Chinese translations from [@tianshuo](https://github.com/tianshuo).\n- German translation from '
            '[@mpbzh](https://github.com/mpbzh) & [@Art4](https://github.com/Art4).\n- Italian translation from '
            '[@azkidenz](https://github.com/azkidenz).\n- Swedish translation from [@magol](https://github.com/magol).'
            '\n- Turkish translation from [@emreerkan](https://github.com/emreerkan).\n- French translation from '
            '[@zapashcanon](https://github.com/zapashcanon).\n- Brazilian Portuguese translation from '
            '[@Webysther](https://github.com/Webysther).\n- Polish translation from '
            '[@amielucha](https://github.com/amielucha) & [@m-aciek](https://github.com/m-aciek).\n- Russian '
            'translation from [@aishek](https://github.com/aishek).\n- Czech translation from '
            '[@h4vry](https://github.com/h4vry).\n- Slovak translation from '
            '[@jkostolansky](https://github.com/jkostolansky).\n- Korean translation from '
            '[@pierceh89](https://github.com/pierceh89).\n- Croatian translation from [@porx](https://github.com/porx).'
            '\n- Persian translation from [@Hameds](https://github.com/Hameds).\n- Ukrainian translation from '
            '[@osadchyi-s](https://github.com/osadchyi-s).\n\n',
            '\n- Start using "changelog" over "change log" since it\'s the common usage.\n- Start versioning based on '
            'the current English version at 0.3.0 to help\n  translation authors keep things up-to-date.\n- Rewrite '
            '"What makes unicorns cry?" section.\n- Rewrite "Ignoring Deprecations" sub-section to clarify the ideal\n'
            '  scenario.\n- Improve "Commit log diffs" sub-section to further argument against\n  them.\n- Merge "Why '
            'canâ€™t people just use a git log diff?" with "Commit log\n  diffs".\n- Fix typos in Simplified Chinese '
            'and Traditional Chinese translations.\n- Fix typos in Brazilian Portuguese translation.\n- Fix typos in '
            'Turkish translation.\n- Fix typos in Czech translation.\n- Fix typos in Swedish translation.\n- Improve '
            'phrasing in French translation.\n- Fix phrasing and spelling in German translation.\n\n',
            '',
            '\n- Section about "changelog" vs "CHANGELOG".',
            '',
            '',
        ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion030(self):
        versionChanges = self.log['0.3.0']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.3.0')])

        answers = ['\n- RU translation from [@aishek](https://github.com/aishek).\n- pt-BR translation from '
                   '[@tallesl](https://github.com/tallesl).\n- es-ES translation from '
                   '[@ZeliosAriex](https://github.com/ZeliosAriex).',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion020(self):
        versionChanges = self.log['0.2.0']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.2.0')])

        answers = ['',
                   '\n- Remove exclusionary mentions of "open source" since this project can\n  benefit both "open" '
                   'and "closed" source projects equally.',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion010(self):
        versionChanges = self.log['0.1.0']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.1.0')])

        answers = ['\n- Answer "Should you ever rewrite a change log?".\n\n',
                   '\n- Improve argument against commit logs.\n- Start following [SemVer](https://semver.org) '
                   'properly.',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion008(self):
        versionChanges = self.log['0.0.8']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.8')])

        answers = ['',
                   '\n- Update year to match in every README example.\n- Reluctantly stop making fun of Brits only, '
                   'since most of the world\n  writes dates in a strange way.\n\n',
                   '',
                   '',
                   '\n- Fix typos in recent README changes.\n- Update outdated unreleased diff link.',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion007(self):
        versionChanges = self.log['0.0.7']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.7')])

        answers = ['\n- Link, and make it obvious that date format is ISO 8601.\n\n',
                   '\n- Clarified the section on "Is there a standard change log format?".\n\n',
                   '',
                   '',
                   '\n- Fix Markdown links to tag comparison URL with footnote-style links.',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion006(self):
        versionChanges = self.log['0.0.6']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.6')])

        answers = ['\n- README section on "yanked" releases.',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion005(self):
        versionChanges = self.log['0.0.5']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.5')])

        answers = ['\n- Markdown links to version tags on release headings.\n- Unreleased section to gather unreleased'
                   ' changes and encourage note\n  keeping prior to releases.',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion004(self):
        versionChanges = self.log['0.0.4']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.4')])

        answers = ['\n- Better explanation of the difference between the file ("CHANGELOG")\n  and its function "the '
                   'change log".\n\n',
                   '\n- Refer to a "change log" instead of a "CHANGELOG" throughout the site\n  to differentiate '
                   'between the file and the purpose of the file â€” the\n  logging of changes.\n\n',
                   '',
                   '\n- Remove empty sections from CHANGELOG, they occupy too much space and\n  create too much noise '
                   'in the file. People will have to assume that the\n  missing sections were intentionally left out '
                   'because they contained no\n  notable changes.',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion003(self):
        versionChanges = self.log['0.0.3']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.3')])

        answers = ['\n- "Why should I care?" section mentioning The Changelog podcast.',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion002(self):
        versionChanges = self.log['0.0.2']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.2')])

        answers = ['\n- Explanation of the recommended reverse chronological release ordering.',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersion001(self):
        versionChanges = self.log['0.0.1']
        self.assertTrue(versionChanges)
        self.assertTrue(self.log[SemanticVersion('0.0.1')])

        answers = ['\n- This CHANGELOG file to hopefully serve as an evolving example of a\n  standardized open source '
                   'project CHANGELOG.\n- CNAME file to enable GitHub Pages custom domain.\n- README now contains '
                   'answers to common questions about CHANGELOGs.\n- Good examples and basic guidelines, including '
                   'proper date formatting.\n- Counter-examples: "What makes unicorns cry?".',
                   '',
                   '',
                   '',
                   '',
                   ''
                   ]
        for change, answer in zip(versionChanges.toDict().values(), answers):
            with self.subTest(msg=change):
                self.assertEqual(change.get('content', ''), answer)

    def testVersionList(self):
        answers = [
            Unreleased,
            SemanticVersion('1.1.1'),
            SemanticVersion('1.1.0'),
            SemanticVersion('1.0.0'),
            SemanticVersion('0.3.0'),
            SemanticVersion('0.2.0'),
            SemanticVersion('0.1.0'),
            SemanticVersion('0.0.8'),
            SemanticVersion('0.0.7'),
            SemanticVersion('0.0.6'),
            SemanticVersion('0.0.5'),
            SemanticVersion('0.0.4'),
            SemanticVersion('0.0.3'),
            SemanticVersion('0.0.2'),
            SemanticVersion('0.0.1'),
        ]

        for answer in answers:
            with self.subTest(msg=answer):
                self.assertIn(answer, self.log)

    def testLinks(self):
        answers = {
            Unreleased: 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.1...HEAD',
            SemanticVersion('1.1.1'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.0...v1.1.1',
            SemanticVersion('1.1.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...v1.1.0',
            SemanticVersion('1.0.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.0...v1.0.0',
            SemanticVersion('0.3.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.0...v0.3.0',
            SemanticVersion('0.2.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0',
            SemanticVersion('0.1.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.8...v0.1.0',
            SemanticVersion('0.0.8'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.7...v0.0.8',
            SemanticVersion('0.0.7'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.6...v0.0.7',
            SemanticVersion('0.0.6'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.5...v0.0.6',
            SemanticVersion('0.0.5'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.4...v0.0.5',
            SemanticVersion('0.0.4'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.3...v0.0.4',
            SemanticVersion('0.0.3'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.2...v0.0.3',
            SemanticVersion('0.0.2'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.1...v0.0.2',
            SemanticVersion('0.0.1'): 'https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1'
        }

        for version, link in answers.items():
            with self.subTest(msg=version):
                self.assertTrue(self.log.links[version], link)

    def testInlineLinks(self):
        answers = {
            Unreleased: 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.1...HEAD',
            SemanticVersion('1.1.1'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.0...v1.1.1',
            SemanticVersion('1.1.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...v1.1.0',
            SemanticVersion('1.0.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.0...v1.0.0',
            SemanticVersion('0.3.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.0...v0.3.0',
            SemanticVersion('0.2.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0',
            SemanticVersion('0.1.0'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.8...v0.1.0',
            SemanticVersion('0.0.8'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.7...v0.0.8',
            SemanticVersion('0.0.7'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.6...v0.0.7',
            SemanticVersion('0.0.6'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.5...v0.0.6',
            SemanticVersion('0.0.5'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.4...v0.0.5',
            SemanticVersion('0.0.4'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.3...v0.0.4',
            SemanticVersion('0.0.3'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.2...v0.0.3',
            SemanticVersion('0.0.2'): 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.1...v0.0.2',
            SemanticVersion('0.0.1'): 'https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1'
        }

        thisDir = pathlib.Path(__file__).parent
        log = Changelog(thisDir / 'inlinelog.md')

        for version, link in answers.items():
            with self.subTest(msg=version):
                self.assertTrue(log.links[version], link)

    def testDictionary(self):
        answer = {'Unreleased':
                      {'version': {},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.1...HEAD',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': "\n- This is where I'd describe what's been added."
                                 },
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '1.1.1':
                      {'version': {'major': 1, 'minor': 1, 'patch': 1, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.0...v1.1.1',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Arabic translation (#444).\n- v1.1 French translation.\n- v1.1 Dutch '
                                            'translation (#371).\n- v1.1 Russian translation (#410).\n- v1.1 Japanese '
                                            'translation (#363).\n- v1.1 Norwegian BokmÃ¥l translation (#383).\n- v1.1 '
                                            '"Inconsistent Changes" Turkish translation (#347).\n- Default to most '
                                            'recent versions available for each languages\n- Display count of available'
                                            ' translations (26 to date!)\n- Centralize all links into '
                                            '`/data/links.json` so they can be updated easily\n\n'},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.\n\n'},
                            'deprecated': {},
                            'removed':
                                {'tag_raw': '### Removed\n',
                                 'content': '\n- Unused normalize.css file\n- Identical links assigned in each '
                                            'translation file\n- Duplicate index file for the english version'},
                            'fixed':
                                {'tag_raw': '### Fixed\n',
                                 'content': "\n- Improve French translation (#377).\n- Improve id-ID translation "
                                            "(#416).\n- Improve Persian translation (#457).\n- Improve Russian "
                                            "translation (#408).\n- Improve Swedish title (#419).\n- Improve zh-CN "
                                            "translation (#359).\n- Improve French translation (#357).\n- Improve "
                                            "zh-TW translation (#360, #355).\n- Improve Spanish (es-ES) transltion "
                                            "(#362).\n- Foldout menu in Dutch translation (#371).\n- Missing periods "
                                            "at the end of each change (#451).\n- Fix missing logo in 1.1 pages\n- "
                                            "Display notice when translation isn't for most recent version\n- Various "
                                            "broken links, page versions, and indentations.\n\n"},
                            'security': {}}},
                  '1.1.0':
                      {'version': {'major': 1, 'minor': 1, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v1.0.0...v1.1.0',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Danish translation (#297).\n- Georgian translation from (#337).\n- '
                                            'Changelog inconsistency section in Bad Practices.\n\n'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed':
                                {'tag_raw': '### Fixed\n',
                                 'content': '\n- Italian translation (#332).\n- Indonesian translation (#336).'},
                            'security': {}}},
                  '1.0.0':
                      {'version': {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.3.0...v1.0.0',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- New visual identity by '
                                            '[@tylerfortune8](https://github.com/tylerfortune8).\n- Version navigation.'
                                            '\n- Links to latest released version in previous versions.\n- "Why keep a '
                                            'changelog?" section.\n- "Who needs a changelog?" section.\n- "How do I '
                                            'make a changelog?" section.\n- "Frequently Asked Questions" section.\n- '
                                            'New "Guiding Principles" sub-section to "How do I make a changelog?".\n- '
                                            'Simplified and Traditional Chinese translations from '
                                            '[@tianshuo](https://github.com/tianshuo).\n- German translation from '
                                            '[@mpbzh](https://github.com/mpbzh) & [@Art4](https://github.com/Art4).\n- '
                                            'Italian translation from [@azkidenz](https://github.com/azkidenz).\n- '
                                            'Swedish translation from [@magol](https://github.com/magol).\n- Turkish '
                                            'translation from [@emreerkan](https://github.com/emreerkan).\n- French '
                                            'translation from [@zapashcanon](https://github.com/zapashcanon).\n- '
                                            'Brazilian Portuguese translation from '
                                            '[@Webysther](https://github.com/Webysther).\n- Polish translation from '
                                            '[@amielucha](https://github.com/amielucha) & '
                                            '[@m-aciek](https://github.com/m-aciek).\n- Russian translation from '
                                            '[@aishek](https://github.com/aishek).\n- Czech translation from '
                                            '[@h4vry](https://github.com/h4vry).\n- Slovak translation from '
                                            '[@jkostolansky](https://github.com/jkostolansky).\n- Korean translation '
                                            'from [@pierceh89](https://github.com/pierceh89).\n- Croatian translation '
                                            'from [@porx](https://github.com/porx).\n- Persian translation from '
                                            '[@Hameds](https://github.com/Hameds).\n- Ukrainian translation from '
                                            '[@osadchyi-s](https://github.com/osadchyi-s).\n\n'},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Start using "changelog" over "change log" since it\'s the common '
                                            'usage.\n- Start versioning based on the current English version at 0.3.0 '
                                            'to help\n  translation authors keep things up-to-date.\n- Rewrite "What '
                                            'makes unicorns cry?" section.\n- Rewrite "Ignoring Deprecations" '
                                            'sub-section to clarify the ideal\n  scenario.\n- Improve "Commit log '
                                            'diffs" sub-section to further argument against\n  them.\n- Merge "Why '
                                            'canâ€™t people just use a git log diff?" with "Commit log\n  diffs".\n- '
                                            'Fix typos in Simplified Chinese and Traditional Chinese translations.\n- '
                                            'Fix typos in Brazilian Portuguese translation.\n- Fix typos in Turkish '
                                            'translation.\n- Fix typos in Czech translation.\n- Fix typos in Swedish '
                                            'translation.\n- Improve phrasing in French translation.\n- Fix phrasing '
                                            'and spelling in German translation.\n\n'},
                            'deprecated': {},
                            'removed':
                                {'tag_raw': '### Removed\n',
                                 'content': '\n- Section about "changelog" vs "CHANGELOG".'},
                            'fixed': {},
                            'security': {}}},
                  '0.3.0':
                      {'version': {'major': 0, 'minor': 3, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.2.0...v0.3.0',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- RU translation from [@aishek](https://github.com/aishek).\n- pt-BR '
                                            'translation from [@tallesl](https://github.com/tallesl).\n- es-ES '
                                            'translation from [@ZeliosAriex](https://github.com/ZeliosAriex).'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.2.0':
                      {'version': {'major': 0, 'minor': 2, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0',
                       'changes':
                           {'added': {},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Remove exclusionary mentions of "open source" since this project can\n'
                                            '  benefit both "open" and "closed" source projects equally.'},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.1.0':
                      {'version': {'major': 0, 'minor': 1, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.8...v0.1.0',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Answer "Should you ever rewrite a change log?".\n\n'},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Improve argument against commit logs.\n- Start following '
                                            '[SemVer](https://semver.org) properly.'},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.0.8':
                      {'version': {'major': 0, 'minor': 0, 'patch': 8, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.7...v0.0.8',
                       'changes':
                           {'added': {},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Update year to match in every README example.\n- Reluctantly stop '
                                            'making fun of Brits only, since most of the world\n  writes dates in a '
                                            'strange way.\n\n'},
                            'deprecated': {},
                            'removed': {},
                            'fixed':
                                {'tag_raw': '### Fixed\n',
                                 'content': '\n- Fix typos in recent README changes.\n- Update outdated unreleased diff'
                                            ' link.'},
                            'security': {}}},
                  '0.0.7':
                      {'version': {'major': 0, 'minor': 0, 'patch': 7, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.6...v0.0.7',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Link, and make it obvious that date format is ISO 8601.\n\n'},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Clarified the section on "Is there a standard change log '
                                            'format?".\n\n'},
                            'deprecated': {},
                            'removed': {},
                            'fixed':
                                {'tag_raw': '### Fixed\n',
                                 'content': '\n- Fix Markdown links to tag comparison URL with footnote-style links.'},
                            'security': {}}},
                  '0.0.6':
                      {'version': {'major': 0, 'minor': 0, 'patch': 6, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.5...v0.0.6',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- README section on "yanked" releases.'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.0.5':
                      {'version': {'major': 0, 'minor': 0, 'patch': 5, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.4...v0.0.5',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Markdown links to version tags on release headings.\n- Unreleased '
                                            'section to gather unreleased changes and encourage note\n  keeping prior '
                                            'to releases.'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.0.4':
                      {'version': {'major': 0, 'minor': 0, 'patch': 4, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.3...v0.0.4',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Better explanation of the difference between the file ("CHANGELOG")\n'
                                            '  and its function "the change log".\n\n'},
                            'changed':
                                {'tag_raw': '### Changed\n',
                                 'content': '\n- Refer to a "change log" instead of a "CHANGELOG" throughout the site\n'
                                            '  to differentiate between the file and the purpose of the file â€” the\n'
                                            '  logging of changes.\n\n'},
                            'deprecated': {},
                            'removed':
                                {'tag_raw': '### Removed\n',
                                 'content': '\n- Remove empty sections from CHANGELOG, they occupy too much space and\n'
                                            '  create too much noise in the file. People will have to assume that the\n'
                                            '  missing sections were intentionally left out because they contained no\n'
                                            '  notable changes.'},
                            'fixed': {},
                            'security': {}}},
                  '0.0.3':
                      {'version': {'major': 0, 'minor': 0, 'patch': 3, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.2...v0.0.3',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- "Why should I care?" section mentioning The Changelog podcast.'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.0.2':
                      {'version': {'major': 0, 'minor': 0, 'patch': 2, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/compare/v0.0.1...v0.0.2',
                       'changes':
                           {'added':
                                {'tag_raw': '### Added\n',
                                 'content': '\n- Explanation of the recommended reverse chronological release '
                                            'ordering.'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}},
                  '0.0.1':
                      {'version': {'major': 0, 'minor': 0, 'patch': 1, 'pre_release': '', 'build_metadata': ''},
                       'link': 'https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1',
                       'changes':
                           {'added': {'tag_raw': '### Added\n',
                                      'content': '\n- This CHANGELOG file to hopefully serve as an evolving example of'
                                                 ' a\n  standardized open source project CHANGELOG.\n- CNAME file to '
                                                 'enable GitHub Pages custom domain.\n- README now contains answers to '
                                                 'common questions about CHANGELOGs.\n- Good examples and basic '
                                                 'guidelines, including proper date formatting.\n- Counter-examples: '
                                                 '"What makes unicorns cry?".'},
                            'changed': {},
                            'deprecated': {},
                            'removed': {},
                            'fixed': {},
                            'security': {}}}}

        self.assertEqual(self.log.toDict(), answer)
