from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout

from jsonlines import Reader, Writer
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='minify',
        description='Minify the code of the OpenAI fine-tuning dataset',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    parse_args()

    with Reader(stdin) as reader:
        dataset = tuple(reader)

    for data in tqdm(dataset):
        content = data['messages'][-1]['content']
        data['messages'][-1]['content'] = ' '.join(content.split())

    with Writer(stdout) as writer:
        writer.write_all(dataset)


if __name__ == '__main__':
    main()
