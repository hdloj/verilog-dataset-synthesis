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
cat data/filtered.jsonl | python describe.py gpt-3.5-turbo 100 > data/descriptions.jsonl
```

Separate module declarations and implementations.

```console
cat data/descriptions.jsonl | python separate.py > data/separated.jsonl
```
