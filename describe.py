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
    'Explain the high-level functionality of the Verilog module. Use as many'
    ' high-level concepts that are directly applicable to describe the code,'
    ' say at the level of an undergraduate EECS major, but do not include'
    ' extraneous details that aren’t immediately applicable. Use text-based'
    ' truth tables and state transition graphs when necessary. Speak concisely'
    ' as if this was a specification for a circuit designer to implement. You'
    ' should only reply with descriptive natural language and not use any'
    ' code.'
)
USER_PROMPT = (
    'Explain the high-level functionality of the Verilog module.\n\n{}'
)
FEW_SHOT_MODULE = '''\
module top_module ( input [7:0] in, output [7:0] out );
    assign out = {in[0], in[1], in[2], in[3], in[4], in[5], in[6], in[7]};
endmodule\
'''
FEW_SHOT_USER_PROMPT = USER_PROMPT.format(FEW_SHOT_MODULE)
FEW_SHOT_ASSISTANT_PROMPT = (
    'This top Verilog module is a 8-bit unidirectional data port. It takes an'
    ' 8-bit input in, and outputs an 8-bit signal out. The output of the'
    ' module is assigned to out based on the value of in. If in ='
    ' a,b,c,d,e,f,g,h, then out = h,g,f,e,d,c,b,a.'
)
BASE_MESSAGES = (
    {'role': 'system', 'content': SYSTEM_PROMPT},
    {'role': 'user', 'content': FEW_SHOT_USER_PROMPT},
    {'role': 'assistant', 'content': FEW_SHOT_ASSISTANT_PROMPT},
)


def parse_args():
    parser = ArgumentParser(
        prog='describe',
        description='Synthesize Verilog module descriptions with OpenAI LLMs',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    parser.add_argument('model', help='OpenAI model to be used', type=str)
    parser.add_argument(
        'max_worker_count',
        help='max number of workers',
        type=int,
    )

    return parser.parse_args()


def describe(client, model, module):
    messages = list(BASE_MESSAGES)
    user_prompt = USER_PROMPT.format(module)

    messages.append({'role': 'user', 'content': user_prompt})

    completion = client.chat.completions.create(model=model, messages=messages)

    return completion.choices[0].message.content


def main():
    load_dotenv()

    args = parse_args()
    client = OpenAI()

    with Reader(stdin) as reader:
        modules = tuple(reader)

    with ThreadPoolExecutor(args.max_worker_count) as executor:
        descriptions = tuple(
            tqdm(
                executor.map(partial(describe, client, args.model), modules),
                total=len(modules),
            ),
        )

    module_descriptions = []

    for module, description in zip(modules, descriptions):
        module_descriptions.append(
            {'module': module, 'description': description},
        )

    with Writer(stdout) as writer:
        writer.write_all(module_descriptions)


if __name__ == '__main__':
    main()
