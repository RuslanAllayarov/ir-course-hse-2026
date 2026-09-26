#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ДЗ 1. Индексация и булев поиск — шаблон решения.

Запуск:
    ./solution.py --build_index --index_dir=index PATH-TO-DATA
    ./solution.py --submission_file=submission.csv --index_dir=index PATH-TO-DATA
"""

import argparse
from timeit import default_timer as timer

from nltk import tokenize


def preprocess(text):
    """Токенизация и нормализация. НЕ МЕНЯЙТЕ эту функцию:
    ей же размечен эталон на Kaggle."""
    tokenizer = tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return [token.lower() for token in tokens]


def build_index(data_dir, index_dir):
    # TODO:
    # - прочитать документы из data_dir/vkmarco-docs.tsv
    #   (без заголовка; поля через таб: DocumentId, URL, Title, Body);
    # - разбить Title и Body на термины функцией preprocess() (URL не индексируем);
    # - построить обратный индекс и сохранить его в index_dir.
    raise NotImplementedError


def make_submission(data_dir, index_dir, submission_file):
    # TODO:
    # - загрузить индекс из index_dir;
    # - прочитать запросы из data_dir/vkmarco-doceval-queries.tsv
    #   (без заголовка; поля через таб: QueryId, QueryText) и разбить их функцией preprocess();
    # - для каждого запроса найти документы, в которых есть ВСЕ термины запроса (И-запрос);
    # - для каждой строки data_dir/objects.csv (ObjectId,QueryId,DocumentId) поставить
    #   Label = 1, если документ нашёлся по запросу, иначе 0;
    # - записать submission_file в формате CSV с заголовком ObjectId,Label.
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description='Boolean retrieval homework solution')
    parser.add_argument('--submission_file', help='куда записать сабмишн для Kaggle')
    parser.add_argument('--build_index', action='store_true', help='режим построения индекса')
    parser.add_argument('--index_dir', required=True, help='папка с индексом')
    parser.add_argument('data_dir', help='папка с данными соревнования')
    args = parser.parse_args()

    start = timer()
    if args.build_index:
        build_index(args.data_dir, args.index_dir)
    else:
        if not args.submission_file:
            parser.error('в режиме генерации сабмишна нужен --submission_file')
        make_submission(args.data_dir, args.index_dir, args.submission_file)
    print(f'finished, elapsed = {timer() - start:.3f}')


if __name__ == '__main__':
    main()
