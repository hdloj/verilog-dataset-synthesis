from argparse import ArgumentParser
from datetime import datetime
from glob import iglob
from pathlib import Path
from sys import stdout

from git import Repo
from jsonlines import Writer
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='extract-git-repo',
        description='Extract verilog code from a local Git repository.',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    parser.add_argument(
        'repo_path',
        type=Path,
        help='path to a local Git repository',
    )

    return parser.parse_args()


def main():
    args = parse_args()
    repo = Repo(args.repo_path)
    sources = []

    for ref in tqdm(repo.remote().refs):
        ref.checkout()

        pathnames = iglob(str(args.repo_path / '**' / '*.v'), recursive=True)

        for path in map(Path, pathnames):
            with open(path, errors='ignore') as file:
                source = file.read()

            sources.append(source)

    with Writer(stdout) as writer:
        writer.write_all(sources)


if __name__ == '__main__':
    main()
