"""Готовит данные для семинара из датасета RuBQ-retrieval.

Источник: https://huggingface.co/datasets/ai-forever/rubq-retrieval (CC BY-SA 4.0).
Скачайте из data/ файлы corpus.jsonl.zip (распакуйте), queries.jsonl, test.jsonl
в папку, путь к которой передаётся первым аргументом:

    python prepare_data.py path/to/rubq

На выходе рядом со скриптом появятся docs.tsv, queries.tsv и qrels.tsv.
"""

import json
import random
import sys
from pathlib import Path

SEED = 42
N_DISTRACTORS = 12_300  # вместе с релевантными получится ~15 тыс. документов
N_DEV = 400             # запросы для подбора параметров, остальные -- test


def clean(text):
    return " ".join(text.replace("\t", " ").replace("\r", " ").replace("\n", " ").split())


def main(src_dir):
    src = Path(src_dir)
    out = Path(__file__).parent

    corpus = [json.loads(line) for line in open(src / "corpus.jsonl", encoding="utf-8")]
    queries = [json.loads(line) for line in open(src / "queries.jsonl", encoding="utf-8")]
    qrels = [json.loads(line) for line in open(src / "test.jsonl", encoding="utf-8")]

    relevant = {row["corpus-id"] for row in qrels}
    others = sorted(doc["_id"] for doc in corpus if doc["_id"] not in relevant)

    rng = random.Random(SEED)
    keep = relevant | set(rng.sample(others, N_DISTRACTORS))

    with open(out / "docs.tsv", "w", encoding="utf-8") as f:
        for doc in corpus:
            if doc["_id"] in keep:
                f.write(f"{doc['_id']}\t{clean(doc['text'])}\n")

    # split: dev -- первые N_DEV запросов после перемешивания с фиксированным seed
    qids = sorted({row["query-id"] for row in qrels}, key=int)
    rng.shuffle(qids)
    split = {qid: ("dev" if i < N_DEV else "test") for i, qid in enumerate(qids)}

    with open(out / "queries.tsv", "w", encoding="utf-8") as f:
        for q in sorted(queries, key=lambda q: int(q["_id"])):
            if q["_id"] in split:
                f.write(f"{q['_id']}\t{split[q['_id']]}\t{clean(q['text'])}\n")

    with open(out / "qrels.tsv", "w", encoding="utf-8") as f:
        for row in qrels:
            f.write(f"{row['query-id']}\t{row['corpus-id']}\n")

    print(f"docs: {len(keep)}, queries: {len(split)} "
          f"(dev {N_DEV}, test {len(split) - N_DEV}), qrels: {len(qrels)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "rubq")
