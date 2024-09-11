from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout

from jsonlines import Reader, Writer
from tqdm import tqdm

PREFIX = (
    'Implement the Verilog module based on the following description. Assume'
    ' that signals are positive clock/clk edge triggered unless otherwise'
    ' stated.'
)


def parse_args():
    parser = ArgumentParser(
        prog='export',
        description='Export the dataset for LLM4HWDesign Phase 1',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    parse_args()

    lines = []

    with Reader(stdin) as reader:
        dataset = tuple(reader)

    for data in tqdm(dataset):
        input_ = data['messages'][1]['content']
        output = data['messages'][2]['content']

        assert input_.startswith(PREFIX)

        input_ = input_[len(PREFIX):].strip()
        line = {
            'input': input_,
            'output': output,
        }

        lines.append(line)

    with Writer(stdout) as writer:
        writer.write_all(lines)


if __name__ == '__main__':
    main()
