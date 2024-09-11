# Verilog Dataset Synthesis

Extract code from third-party sources.

```console
python extract-git-repo.py ip-cores/ > data/ip-cores.jsonl
python extract-git-repo.py index-librorum-prohibitorum/ > data/index-librorum-prohibitorum.jsonl
python extract-mg-verilog.py > data/mg-verilog.jsonl
```

Merge and deduplicate extracted code.

```console
cat data/*.jsonl | sort | uniq > data/concatenated.jsonl
```

Download and save [Verible](https://github.com/chipsalliance/verible) executables in the ``bin/`` folder. Add the ``bin/`` folder to ``PATH``.

```console
export PATH=$PATH:bin/
```

Format and deduplicate code.

```console
cat data/concatenated.jsonl | python format.py | sort | uniq > data/formatted.jsonl
```

Collect and deduplicate modules.

```console
cat data/formatted.jsonl | python module.py | sort | uniq > data/modules.jsonl
```

Filter out modules whose number of lines exceed 200.

```console
cat data/modules.jsonl | python filter.py 200 > data/filtered.jsonl
```

Generate module descriptions. Set the maximum number of workers depending on the OpenAI account usage tier.

```console
cat data/filtered.jsonl | python describe.py [model] [max-worker-count] > data/descriptions.jsonl
```

Separate module declarations and implementations.

```console
cat data/descriptions.jsonl | python separate.py > data/separated.jsonl
```

Create fine-tuning dataset for OpenAI.

```console
cat data/separated.jsonl | python fine-tuning-openai.py > data/openai.jsonl
```

(Optionally) Create a minified version of the fine-tuning dataset.

```console
cat data/openai.jsonl | python minify.py > data/openai-minified.jsonl
```

Solve VerilogEval problems.

```console
cat data/verilog-eval-machine.jsonl | python verilog-eval-openai.py [model] [max-worker-count] [k] > data/solutions-machine.jsonl
cat data/verilog-eval-human.jsonl | python verilog-eval-openai.py [model] [max-worker-count] [k] > data/solutions-human.jsonl
```

Export dataset for fine-tuning.

```console
cat data/openai.jsonl | python export.py > exported.jsonl
```
