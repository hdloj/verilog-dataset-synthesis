from argparse import ArgumentParser
from datetime import datetime
from sys import stdout
import re

from datasets import load_dataset
from jsonlines import Writer
from tqdm import tqdm

DATASET_PATH = 'GaTech-EIC/MG-Verilog'
MODULE_HEADER_PATTERN = re.compile(
    r'(?<=Module header:).*(?=\[\/INST\])',
    re.DOTALL,
)


def parse_args():
    parser = ArgumentParser(
        prog='extract-mg-verilog',
        description='Extract verilog code from the MG-Verilog dataset.',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    _ = parse_args()
    dataset = load_dataset(DATASET_PATH)
    training_set = dataset['train']
    sources = []

    for row in tqdm(training_set):
        code = row['code']
        description = row['description']['high_level_global_summary']
        m = re.search(MODULE_HEADER_PATTERN, description)

        assert m is not None

        sources.append(m[0] + code)

    with Writer(stdout) as writer:
        writer.write_all(sources)


if __name__ == '__main__':
    main()
