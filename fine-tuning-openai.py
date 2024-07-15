from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout

from jsonlines import Reader, Writer
from tqdm import tqdm

SYSTEM_PROMPT = (
    'You only complete chats with syntax correct Verilog code. End the Verilog'
    ' module code completion with \'endmodule\'. Do not include module, input'
    ' and output definitions.'
)
USER_PROMPT = (
    'Implement the Verilog module based on the following description. Assume'
    ' that signals are positive clock/clk edge triggered unless otherwise'
    ' stated.\n\n{}\n\nModule header:\n\n{}'
)


def parse_args():
    parser = ArgumentParser(
        prog='fine-tuning-openai',
        description=(
            'Create OpenAI fine-tuning dataset using module declarations,'
            ' implementations, and descriptions.'
        ),
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    parse_args()

    with Reader(stdin) as reader:
        module_descriptions = tuple(reader)

    dataset = []

    for module_description in tqdm(module_descriptions):
        module = module_description['module']
        declaration = module['declaration']
        implementation = module['implementation']
        description = module_description['description']
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {
                'role': 'user',
                'content': USER_PROMPT.format(description, declaration),
            },
            {'role': 'assistant', 'content': implementation},
        ]

        dataset.append({'messages': messages})

    with Writer(stdout) as writer:
        writer.write_all(dataset)


if __name__ == '__main__':
    main()
