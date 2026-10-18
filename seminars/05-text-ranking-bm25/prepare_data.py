"""Готовит подвыборку MIRACL (ru) для семинара «Текстовое ранжирование. Часть II».

Источник: https://huggingface.co/datasets/miracl/miracl (запросы и оценки)
          https://huggingface.co/datasets/miracl/miracl-corpus (корпус), лицензия Apache-2.0.

Берём dev-запросы, все размеченные пассажи (и релевантные, и размеченные нерелевантные)
и детерминированную случайную выборку остальных пассажей по хешу docid.
Корпус (~2 ГБ gz) читается потоком, на диск целиком не сохраняется.

Запуск: python prepare_data.py  (результат пишется рядом со скриптом)
"""
import gzip
import hashlib
import json
import random
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = "https://huggingface.co/datasets/miracl/miracl/resolve/main/miracl-v1.0-ru"
CORPUS = "https://huggingface.co/datasets/miracl/miracl-corpus/resolve/main/miracl-corpus-v1.0-ru/docs-{}.jsonl.gz"
N_FILES = 20
DISTRACTOR_RATE = 85 / 100_000   # ~8 тыс. случайных пассажей из ~9.5 млн
N_DEV = 400                      # запросы для подбора параметров, остальные -- test
SEED = 42

OUT = Path(__file__).resolve().parent


def fetch_text(url):
    with urllib.request.urlopen(url) as r:
        return r.read().decode("utf-8")


def clean(text):
    return " ".join(text.replace("\t", " ").split())


def is_distractor(docid):
    h = int(hashlib.md5(docid.encode()).hexdigest()[:8], 16)
    return h / 0xFFFFFFFF < DISTRACTOR_RATE


def scan(i, judged):
    found = {}
    with urllib.request.urlopen(CORPUS.format(i)) as r, gzip.open(r, "rt", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if d["docid"] in judged or is_distractor(d["docid"]):
                found[d["docid"]] = (clean(d["title"]), clean(d["text"]))
    print(f"файл {i}: {len(found)} пассажей", flush=True)
    return found


def main():
    topics = [l.split("\t", 1) for l in fetch_text(f"{BASE}/topics/topics.miracl-v1.0-ru-dev.tsv").splitlines() if l]
    qrels = [l.split("\t") for l in fetch_text(f"{BASE}/qrels/qrels.miracl-v1.0-ru-dev.tsv").splitlines() if l]
    judged = {docid for _, _, docid, _ in qrels}
    print(f"запросов: {len(topics)}, оценок: {len(qrels)}, размеченных пассажей: {len(judged)}")

    docs = {}
    with ThreadPoolExecutor(4) as pool:
        for part in pool.map(lambda i: scan(i, judged), range(N_FILES)):
            docs.update(part)
    missing = judged - docs.keys()
    assert not missing, f"не нашли {len(missing)} размеченных пассажей"

    with open(OUT / "docs.tsv", "w", encoding="utf-8") as f:
        for docid in sorted(docs):
            title, text = docs[docid]
            f.write(f"{docid}\t{title}\t{text}\n")

    qids = sorted(int(q) for q, _ in topics)
    random.Random(SEED).shuffle(qids)
    dev = set(qids[:N_DEV])
    with open(OUT / "queries.tsv", "w", encoding="utf-8") as f:
        for q, text in sorted(topics, key=lambda t: int(t[0])):
            f.write(f"{q}\t{'dev' if int(q) in dev else 'test'}\t{clean(text)}\n")

    with open(OUT / "qrels.tsv", "w", encoding="utf-8") as f:
        for q, _, docid, rel in qrels:
            f.write(f"{q}\t{docid}\t{rel}\n")
    print(f"документов: {len(docs)} (размеченных {len(judged)}, случайных {len(docs) - len(judged)})")


if __name__ == "__main__":
    main()
