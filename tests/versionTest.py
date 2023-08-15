import unittest
from copy import deepcopy

from changelog_handler import SemanticVersion, InvalidSemanticVersion

class VersionTest(unittest.TestCase):

    def equalDicts(self, lhs: dict, rhs: dict) -> bool:
        for kl, kr in zip(lhs, rhs):
            if lhs[kl] != rhs[kr]:
                return False

        return True

    def testParsing(self):
        tests = [
            '1.2.3',
            'v0.1.2',
            'V2.0.5',
            '1.0.0-alpha',
            '1.0.0-alpha.1',
            '1.0.0-0.3.7',
            '1.0.0-x.7.z.92',
            '1.0.0-x-y-z.--',
            '1.0.0-alpha+001',
            '1.0.0+20130313144700',
            '1.0.0-beta+exp.sha.5114f85',
            '1.0.0+21AF26D3----117B344092BD'
        ]
        answers = [
            {'major': 1, 'minor': 2, 'patch': 3, 'pre_release': '', 'build_metadata': ''},
            {'major': 0, 'minor': 1, 'patch': 2, 'pre_release': '', 'build_metadata': ''},
            {'major': 2, 'minor': 0, 'patch': 5, 'pre_release': '', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha.1', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': '0.3.7', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'x.7.z.92', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'x-y-z.--', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha', 'build_metadata': '001'},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': '', 'build_metadata': '20130313144700'},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'beta', 'build_metadata': 'exp.sha.5114f85'},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': '', 'build_metadata': '21AF26D3----117B344092BD'},
        ]
        for test, ans in zip(tests, answers):
            with self.subTest(test=test):
                v = SemanticVersion(test)
                self.assertEqual(v.toDict(), ans)

    def testInvalidVersions(self):
        tests = [
            '1.0',
            '1..0',
            '1.2.3alpha',
            '1.0.0-',
            '1.0.0+'
        ]
        for test in tests:
            with self.subTest(test=test):
                with self.assertRaises(InvalidSemanticVersion):
                    v = SemanticVersion(test)

    def testOrder(self):
        vStrings = [
            '1.0.0-alpha',
            '1.0.0-alpha.1',
            '1.0.0-alpha.beta',
            '1.0.0-beta',
            '1.0.0-beta.2',
            '1.0.0-beta.11',
            '1.0.0-rc.1',
            '1.0.0',
            '1.0.1',
            '1.1.0',
            '1.1.1',
            '1.0.1-alpha.beta',
            '1.0.0-rc+5F23C7',
        ]
        versions = sorted([SemanticVersion(s) for s in vStrings])

        answers = [
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha.1', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'alpha.beta', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'beta', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'beta.2', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'beta.11', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'rc', 'build_metadata': '5F23C7'},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': 'rc.1', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 1, 'pre_release': 'alpha.beta', 'build_metadata': ''},
            {'major': 1, 'minor': 0, 'patch': 1, 'pre_release': '', 'build_metadata': ''},
            {'major': 1, 'minor': 1, 'patch': 0, 'pre_release': '', 'build_metadata': ''},
            {'major': 1, 'minor': 1, 'patch': 1, 'pre_release': '', 'build_metadata': ''},
        ]

        for version, answer in zip(versions, answers):
            with self.subTest(version=version):
                self.assertEqual(version.toDict(), answer)

    def testEquality(self):
        versions = [
            SemanticVersion('v1.0.0'),
            SemanticVersion('1.0.0-alpha'),
            SemanticVersion('1.0.0+ABD-123'),
            SemanticVersion('1.0.0-alpha+dev2'),
        ]

        copies = deepcopy(versions)

        for v, c in zip(versions, copies):
            with self.subTest(version=v):
                self.assertEqual(v, c)

if __name__ == '__main__':
    unittest.main()
