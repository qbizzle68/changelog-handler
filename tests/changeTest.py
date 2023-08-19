import unittest

from changelog_handler import Changes


class ChangeTest(unittest.TestCase):

    string = '''### Added

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

### Fixed

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
- Various broken links, page versions, and indentations.

### Changed

- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.

### Removed

- Unused normalize.css file
- Identical links assigned in each translation file
- Duplicate index file for the english version

### Deprecated

- blah
- blah
- blah

### Security

- fixed y2k issues

'''
    
    def testChanges(self):
        change = Changes(self.string)
        self.assertEqual(change.added, {'tag_raw': '### Added\n', 'content': '''
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

'''})
        self.assertEqual(change.fixed, {'tag_raw': '### Fixed\n', 'content': '''
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
- Various broken links, page versions, and indentations.

'''})
        self.assertEqual(change.changed, {'tag_raw': '### Changed\n', 'content': '''
- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.

'''})
        self.assertEqual(change.removed, {'tag_raw': '### Removed\n', 'content': '''
- Unused normalize.css file
- Identical links assigned in each translation file
- Duplicate index file for the english version

'''})
        self.assertEqual(change.deprecated, {'tag_raw': '### Deprecated\n', 'content': '''
- blah
- blah
- blah

'''})
        self.assertEqual(change.security, {'tag_raw': '### Security\n', 'content': '''
- fixed y2k issues

'''})

    def testDict(self):
        change = Changes(self.string)
        self.assertEqual(change.toDict(), {'added': {'tag_raw': '### Added\n', 'content': '''
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

'''}, 'fixed': {'tag_raw': '### Fixed\n', 'content': '''
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
- Various broken links, page versions, and indentations.

'''}, 'changed': {'tag_raw': '### Changed\n', 'content': '''
- Upgrade dependencies: Ruby 3.2.1, Middleman, etc.

'''}, 'removed': {'tag_raw': '### Removed\n', 'content': '''
- Unused normalize.css file
- Identical links assigned in each translation file
- Duplicate index file for the english version

'''}, 'deprecated': {'tag_raw': '### Deprecated\n', 'content': '''
- blah
- blah
- blah

'''}, 'security': {'tag_raw': '### Security\n', 'content': '''
- fixed y2k issues

'''}})
