from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from sys import stdin, stdout

from dotenv import load_dotenv
from jsonlines import Reader, Writer
from openai import OpenAI
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
        prog='verilog-eval-openai',
        description='Evaluate verilog-eval problems.',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    parser.add_argument('model', help='OpenAI model to be used', type=str)
    parser.add_argument(
        'max_worker_count',
        help='max number of workers',
        type=int,
    )
    parser.add_argument('k', help='k value in pass@k', type=int)

    return parser.parse_args()


def solve(client, model, problem):
    task_id = problem['task_id']
    module = problem['module']
    declaration = module['declaration']
    description = problem['description']
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {
            'role': 'user',
            'content': USER_PROMPT.format(description, declaration),
        },
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return {
        'task_id': task_id,
        'completion': completion.choices[0].message.content,
    }


def main():
    load_dotenv()

    args = parse_args()
    client = OpenAI()

    with Reader(stdin) as reader:
        problems = tuple(reader)

    problems *= args.k

    with ThreadPoolExecutor(args.max_worker_count) as executor:
        solutions = tuple(
            tqdm(
                executor.map(partial(solve, client, args.model), problems),
                total=len(problems),
            ),
        )

    with Writer(stdout) as writer:
        writer.write_all(solutions)


if __name__ == '__main__':
    main()
