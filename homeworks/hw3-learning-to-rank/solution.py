#!/usr/bin/env python
# ДЗ 3. Обучение ранжированию — шаблон решения.
#
# Обучение:  ./solution.py --train --model_file=model.bin PATH-TO-DATA
# Сабмишн:   ./solution.py --model_file=model.bin --submission_file=submission.csv PATH-TO-DATA

import argparse
import os
from timeit import default_timer as timer

import pandas as pd


def train(data_dir, model_file):
    data = pd.read_csv(os.path.join(data_dir, 'train.csv'))
    features = [column for column in data.columns if column not in ('QueryId', 'Label')]

    # TODO:
    # - отложить часть запросов (целиком, не отдельные строки) и сравнивать варианты по nDCG@10 на них;
    # - обучить модель ранжирования на data[features] и data['Label'], группы — data['QueryId'];
    # - сохранить модель в model_file.


def predict(data_dir, model_file, submission_file):
    test = pd.read_csv(os.path.join(data_dir, 'test.csv'))
    features = [column for column in test.columns if column not in ('ObjectId', 'QueryId')]

    # TODO: загрузить модель из model_file и посчитать скор для каждой строки test[features].
    scores = [0.0] * len(test)  # замените своими скорами

    submission = pd.DataFrame({'ObjectId': test['ObjectId'], 'Score': scores})
    submission.to_csv(submission_file, index=False)


def main():
    parser = argparse.ArgumentParser(description='Learning to rank homework solution')
    parser.add_argument('--train', action='store_true', help='обучить модель и сохранить её в model_file')
    parser.add_argument('--model_file', required=True, help='файл модели')
    parser.add_argument('--submission_file', help='куда записать сабмишн для Kaggle')
    parser.add_argument('data_dir', help='папка с данными соревнования')
    args = parser.parse_args()

    start = timer()

    # Если в решении есть случайность, зафиксируйте seed: random_seed у CatBoost, seed у LightGBM и т. п.

    if args.train:
        train(args.data_dir, args.model_file)
    else:
        if args.submission_file is None:
            parser.error('без --train нужен --submission_file')
        predict(args.data_dir, args.model_file, args.submission_file)

    print(f'finished, elapsed = {timer() - start:.3f}')


if __name__ == '__main__':
    main()
