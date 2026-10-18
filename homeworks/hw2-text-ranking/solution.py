#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ДЗ 2. Текстовое ранжирование — шаблон решения.

Запуск:
    ./solution.py --submission_file=submission.csv PATH-TO-DATA
"""

import argparse
import csv
import os
from timeit import default_timer as timer


def read_queries(path):
    """QueryId -> QueryText."""
    queries = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            query_id, text = line.rstrip('\n').split('\t', 1)
            queries[int(query_id)] = text
    return queries


def read_qrels(path):
    """QueryId -> {DocumentId -> Label}. Формат строки: QueryId 0 DocumentId Label."""
    qrels = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            query_id, _, doc_id, label = line.split()
            qrels.setdefault(int(query_id), {})[doc_id] = int(label)
    return qrels


def read_docs(path, doc_ids=None):
    """DocumentId -> (URL, Title, Body). Если передан doc_ids, читает только эти документы."""
    docs = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            fields = line.rstrip('\n').split('\t')
            fields += [''] * (4 - len(fields))
            doc_id, url, title, body = fields[:4]
            if doc_ids is None or doc_id in doc_ids:
                docs[doc_id] = (url, title, body)
    return docs


def main():
    parser = argparse.ArgumentParser(description='Text ranking homework solution')
    parser.add_argument('--submission_file', required=True, help='куда записать сабмишн для Kaggle')
    parser.add_argument('data_dir', help='папка с данными соревнования')
    args = parser.parse_args()

    start = timer()

    # Если в решении есть случайность, зафиксируйте seed:
    # random.seed(42)
    # np.random.seed(42)

    train_queries = read_queries(os.path.join(args.data_dir, 'vkmarco-doctrain-queries.tsv'))
    train_qrels = read_qrels(os.path.join(args.data_dir, 'vkmarco-doctrain-qrels.tsv'))
    test_queries = read_queries(os.path.join(args.data_dir, 'vkmarco-doceval-queries.tsv'))
    with open(os.path.join(args.data_dir, 'objects.csv'), encoding='utf-8') as f:
        objects = [(int(r['ObjectId']), int(r['QueryId']), r['DocumentId']) for r in csv.DictReader(f)]

    # TODO:
    # - прочитать документы (read_docs), токенизировать и нормализовать Title и Body;
    # - реализовать ранжирующую функцию: TF-IDF, BM25, BM25F, языковую модель и т. п.;
    # - подобрать её параметры по nDCG@10 на train_queries / train_qrels;
    # - посчитать скор для каждой пары (QueryId, DocumentId) из objects.

    scores = {object_id: 0.0 for object_id, _, _ in objects}  # замените своими скорами

    with open(args.submission_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ObjectId', 'Score'])
        for object_id, _, _ in objects:
            writer.writerow([object_id, scores[object_id]])

    print(f'finished, elapsed = {timer() - start:.3f}')


if __name__ == '__main__':
    main()
