from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout
import re

from jsonlines import Reader, Writer
from tqdm import tqdm

DECLARATION_PATTERN = re.compile(
    r'^\s*?module\b.*?;',
    re.MULTILINE | re.DOTALL,
)


def parse_args():
    parser = ArgumentParser(
        prog='separate',
        description='Separate Verilog module declaration and implementation',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def separate(line):
    if isinstance(line, str):
        module = line
    elif isinstance(line, dict):
        module = line['module']
    else:
        raise ValueError(f'unknown type {repr(type(line).__name__)}')

    m = re.match(DECLARATION_PATTERN, module)

    assert m is not None, module

    declaration = m.group()
    implementation = module[m.end():]

    assert declaration + implementation == module

    module = {
        'declaration': declaration,
        'implementation': implementation,
    }

    if isinstance(line, str):
        return module
    elif isinstance(line, dict):
        line['module'] = module

        return line
    else:
        raise AssertionError


def main():
    parse_args()

    with Reader(stdin) as reader:
        lines = list(reader)

    separated_lines = []

    for line in tqdm(lines):
        try:
            separated_line = separate(line)
        except:  # noqa: E722
            pass
        else:
            separated_lines.append(separated_line)

    with Writer(stdout) as writer:
        writer.write_all(separated_lines)


if __name__ == '__main__':
    main()
