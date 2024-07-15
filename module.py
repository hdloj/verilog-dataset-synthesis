from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout
import re

from jsonlines import Reader, Writer
from tqdm import tqdm

PATTERN = re.compile(
    r'^\s*?module\b.*?^\s*?endmodule\b',
    re.MULTILINE | re.DOTALL,
)
HEADER_PATTERN = re.compile(r'^\s*?module\b', re.MULTILINE)
FOOTER_PATTERN = re.compile(r'^\s*?endmodule\b', re.MULTILINE)


def parse_args():
    parser = ArgumentParser(
        prog='module',
        description='Extract modules from Verilog source code',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    parse_args()

    with Reader(stdin) as reader:
        sources = tuple(reader)

    modules = []

    for source in tqdm(sources):
        modules.extend(map(str.strip, re.findall(PATTERN, source)))

    with Writer(stdout) as writer:
        for module in modules:
            if (
                    len(re.findall(HEADER_PATTERN, module)) == 1
                    and len(re.findall(FOOTER_PATTERN, module)) == 1
            ):
                writer.write(module)


if __name__ == '__main__':
    main()
