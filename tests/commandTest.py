import argparse
import os
import pathlib
import subprocess
import sys
import unittest
import contextlib
import io
import changelog_handler

from changelog_handler.__main__ import CheckUniqueTags, DEFAULT_TAG_ORDER, createParser, getChangelogPath, \
    getTagOrder, printChanges


@contextlib.contextmanager
def assertRaisesQuietly(testCase: unittest.TestCase):
    with testCase.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
        yield None


@contextlib.contextmanager
def prohibitExit():
    try:
        yield None
    except SystemExit:
        pass


@contextlib.contextmanager
def manageOutput(buffer: io.StringIO):
    sys.stdout = buffer
    try:
        yield None
    finally:
        sys.stdout = sys.__stdout__


class CommandTest(unittest.TestCase):

    def testTagClass(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--tag-order', nargs='+', choices=DEFAULT_TAG_ORDER, action=CheckUniqueTags, type=str.lower)

        tests = [
            ['added'],
            ['removed', 'deprecated'],
            ['security', 'removed', 'fixed'],
            ['changed', 'removed', 'fixed', 'security'],
            ['added', 'security', 'deprecated', 'fixed', 'removed'],
            ['fixed', 'added', 'removed', 'deprecated', 'security', 'changed'],
        ]

        for test in tests:
            with self.subTest(msg=test):
                self.assertTrue(parser.parse_args(['--tag-order'] + test))

        with assertRaisesQuietly(self):
            parser.parse_args(['--tag-order', 'added', 'added'])

        with assertRaisesQuietly(self):
            parser.parse_args(['--tag-order', 'added', 'foo'])

    def testParser(self):
        parser = createParser()

        with prohibitExit(), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(parser.parse_args(['--version']), f'changelog_handler {changelog_handler.__version__}')

        with prohibitExit():
            args = parser.parse_args(['1.0.0', '--prepend', '# v1.0.0\n## changelog_handler v1.0.0'])
            self.assertEqual(args.prepend, '# v1.0.0\n## changelog_handler v1.0.0')

        with assertRaisesQuietly(self):
            parser.parse_args(['1.0.0', '--changelog-dir', 'foo', '--changelog-path', 'bar'])

    def testChangelogPath(self):
        parser = createParser()

        with prohibitExit():
            args = parser.parse_args(['1.0.0'])
        path = pathlib.Path.cwd() / 'CHANGELOG.md'
        self.assertEqual(getChangelogPath(args), path)

        with prohibitExit():
            args = parser.parse_args(['1.0.0', '--changelog-dir', 'foo/bar'])
        path = pathlib.Path('foo/bar/CHANGELOG.md')
        self.assertEqual(getChangelogPath(args), path)

        with prohibitExit():
            args = parser.parse_args(['1.0.0', '--changelog-dir', r'foo\bar'])
        path = pathlib.Path('foo/bar/CHANGELOG.md')
        self.assertEqual(getChangelogPath(args), path)

        with prohibitExit():
            args = parser.parse_args(['1.0.0', '--changelog-path', 'foo/bar/baz.md'])
        path = pathlib.Path('foo/bar/baz.md')
        self.assertEqual(getChangelogPath(args), path)

        with prohibitExit():
            args = parser.parse_args(['1.0.0', '--changelog-path', r'foo\bar\baz.md'])
        path = pathlib.Path('foo/bar/baz.md')
        self.assertEqual(getChangelogPath(args), path)

    def testTagOrder(self):
        parser = createParser()

        tests = [
            ['added'],
            ['removed', 'deprecated'],
            ['security', 'removed', 'fixed'],
            ['changed', 'removed', 'fixed', 'security'],
            ['added', 'security', 'deprecated', 'fixed', 'removed'],
            ['fixed', 'added', 'removed', 'deprecated', 'security', 'changed'],
        ]

        answers = [
            ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security'],
            ['removed', 'deprecated', 'added', 'changed', 'fixed', 'security'],
            ['security', 'removed', 'fixed', 'added', 'changed', 'deprecated'],
            ['changed', 'removed', 'fixed', 'security', 'added', 'deprecated'],
            ['added', 'security', 'deprecated', 'fixed', 'removed', 'changed'],
            ['fixed', 'added', 'removed', 'deprecated', 'security', 'changed']
        ]

        for test, answer in zip(tests, answers):
            with prohibitExit(), self.subTest(msg=test):
                args = parser.parse_args(['1.0.0', '--tag-order'] + test)
                ans = getTagOrder(args)
                self.assertEqual(ans, answer)

    def testPrinting(self):
        changeStr = '### Added\n- one change\n- another change\n\n### Fixed\n- nothing, we\'re perfect\n'
        changes = changelog_handler.Changes(changeStr)
        link = '[1.0.0]: example.com'
        tag_order = DEFAULT_TAG_ORDER
        heading = '# v1.0.0\n## changelog_handler v1.0.0\n'

        # Set the print string to a custom buffer to check the output.
        buffer = io.StringIO()
        with manageOutput(buffer):
            printChanges(changes, link, tag_order, heading=heading)
        answer = heading + changeStr + f'\n\n{link}'
        self.assertEqual(buffer.getvalue(), answer)

        # Create a temporary directory for output file.
        outputFile = pathlib.Path('temp-changelog_handler-output-test/changes.md')
        if not outputFile.exists():
            os.mkdir(outputFile.parent)
        # Print to the file.
        printChanges(changes, link, tag_order, file=outputFile, heading=heading)
        with open(outputFile, 'r') as f:
            data = f.read()
            self.assertEqual(data, answer)
        # Remove temporarily created files.
        os.remove(outputFile)
        outputFile.parent.rmdir()

    def testCommandLine(self):
        # Version 0.0.7 will be used because it has single line outputs and reduces the
        # size of this file.
        args = ['python', '-m', 'changelog_handler', '0.0.7', '--changelog-path', 'tests\\testlog.md']

        proc = subprocess.run(args + ['python', '-m', 'changelog_handler', '--version'], text=True,
                              stdout=subprocess.PIPE)
        self.assertEqual(proc.stdout, f'changelog_handler {changelog_handler.__version__}\n')

        proc = subprocess.run(args, text=True, stdout=subprocess.PIPE)
        self.assertEqual(proc.stdout, '### Added\n\n- Link, and make it obvious that date format is ISO 8601.\n\n### '
                                      'Changed\n\n- Clarified the section on "Is there a standard change log format?".'
                                      '\n\n### Fixed\n\n- Fix Markdown links to tag comparison URL with footnote-style '
                                      'links.')

        proc = subprocess.run(args + ['--tag-order', 'changed'], text=True, stdout=subprocess.PIPE)
        self.assertEqual(proc.stdout, '### Changed\n\n- Clarified the section on "Is there a standard change log '
                                      'format?".\n\n### Added\n\n- Link, and make it obvious that date format is ISO '
                                      '8601.\n\n### Fixed\n\n- Fix Markdown links to tag comparison URL with '
                                      'footnote-style links.')

        proc = subprocess.run(args + ['--prepend', '## [0.0.7] - 2015-02-16\n'], text=True, stdout=subprocess.PIPE)
        self.assertEqual(proc.stdout, '## [0.0.7] - 2015-02-16\n### Added\n\n- Link, and make it obvious that date '
                                      'format is ISO 8601.\n\n### Changed\n\n- Clarified the section on "Is there a '
                                      'standard change log format?".\n\n### Fixed\n\n- Fix Markdown links to tag '
                                      'comparison URL with footnote-style links.')

        proc = subprocess.run(args + ['--add-link'], text=True, stdout=subprocess.PIPE)
        self.assertEqual(proc.stdout, '### Added\n\n- Link, and make it obvious that date format is ISO 8601.\n\n### '
                                      'Changed\n\n- Clarified the section on "Is there a standard change log format?".'
                                      '\n\n### Fixed\n\n- Fix Markdown links to tag comparison URL with footnote-style '
                                      'links.\n\n[0.0.7]: https://github.com/olivierlacan/keep-a-changelog/compare/'
                                      'v0.0.6...v0.0.7')
