import argparse
import pathlib
import platform
import sys

from . import __version__, SemanticVersion, Changelog, Changes


class CheckUniqueTags(argparse.Action):
    """Checks that the list of arguments contains no duplicates."""

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > len(set(values)):
            duplicate = [v for v in values]
            for v in set(values):
                duplicate.remove(v)
            raise argparse.ArgumentError(
                self,
                f"You cannot specify the same tag multiple times. Duplicates found: {duplicate}"
            )
        setattr(namespace, self.dest, values)


def correctOption(string):
    """Handle the input string based on OS type."""

    if platform.system() == 'Windows':
        # Windows escaped newline character needs to be replaced.
        return string.replace('\\n', '\n')

    return string


DEFAULT_TAG_ORDER = ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security']


def createParser() -> argparse.ArgumentParser:
    """Create the ArgumentParser object for this script."""

    parser = argparse.ArgumentParser(description='Parse a change log for specific version changes.', prog=__package__)
    parser.add_argument('version', help='the version to parse the changelog for', type=SemanticVersion)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-o', '--output-path', help='path to output changes to', type=pathlib.Path, default=None)
    parser.add_argument('-t', '--tag-order', help='order that change tags will appear', nargs='+',
                        choices=DEFAULT_TAG_ORDER, action=CheckUniqueTags, type=str.lower)
    parser.add_argument('--prepend', help='optional heading to prepend before outputting changes',
                        type=correctOption)
    parser.add_argument('--add-link', help='append the link to the version found in the change log',
                        action='store_true')

    changeGroup = parser.add_mutually_exclusive_group()
    changeGroup.add_argument('-d', '--changelog-dir', help='path to the directory to search for CHANGELOG.md',
                             type=pathlib.Path)
    changeGroup.add_argument('-p', '--changelog-path', type=pathlib.Path,
                             help='path to the change log; use this to specify an alternate filename')

    return parser


def getChangelogPath(args: argparse.Namespace) -> pathlib.Path:
    """Determine path to the change log based on optional arguments."""

    # Determine the location of the change log file.
    currentWorkingDirectory = pathlib.Path.cwd()
    if args.changelog_dir:
        changelogPath = args.changelog_dir / 'CHANGELOG.md'
    elif args.changelog_path:
        changelogPath = args.changelog_path
    else:
        changelogPath = currentWorkingDirectory / 'CHANGELOG.md'

    return changelogPath


def getTagOrder(args: argparse.Namespace) -> list[str]:
    """Set the order to output changes."""

    if args.tag_order:
        if len(args.tag_order) == 6:
            tag_order = args.tag_order
        elif args.tag_order == DEFAULT_TAG_ORDER:
            tag_order = DEFAULT_TAG_ORDER
        else:
            tag_order = [t for t in args.tag_order]
            for tag in DEFAULT_TAG_ORDER:
                if tag not in tag_order:
                    tag_order.append(tag)
    else:
        tag_order = DEFAULT_TAG_ORDER

    return tag_order


def _print(output, file, heading):
    if heading:
        print(heading, end='', file=file)
    print(output, end='', file=file)


def printChanges(changes: Changes, link: str, tagOrder: list[str], file=None, heading=None):
    """Handle the actual outputting of changes."""

    output = ''
    for tag in tagOrder:
        attr = getattr(changes, tag)
        if attr:
            output += attr['tag_raw']
            output += attr['content']

    if link:
        output += f'\n\n{link}'

    if file:
        with open(file, 'w') as f:
            _print(output, f, heading)
    else:
        _print(output, None, heading)


def main():
    parser = createParser()
    args = parser.parse_args()

    changelogPath = getChangelogPath(args)
    log = Changelog(changelogPath)
    changes = log[args.version]

    tagOrder = getTagOrder(args)
    outputPath = args.output_path
    heading = args.prepend

    if args.add_link:
        link = '[{0}]: {1}'.format(args.version, log.links.get(args.version, ''))
    else:
        link = ''
    printChanges(changes, link, tagOrder, file=outputPath, heading=heading)

    return 0


if __name__ == '__main__':
    sys.exit(main())
