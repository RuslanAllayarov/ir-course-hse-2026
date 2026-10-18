# Семинар: текстовое ранжирование, часть I

Ноутбук `tfidf_seminar.ipynb`: TF-IDF руками и в `sklearn`, варианты взвешивания, русская морфология (и чистка знаков ударения),
кворум, `whoosh` (TF-IDF против BM25F), псевдорелевантная обратная связь и LSA. В конце задания.


## Данные

Подвыборка датасета RuBQ-retrieval: https://huggingface.co/datasets/ai-forever/rubq-retrieval
(абзацы русской Википедии и вопросы к ним, входит в ruMTEB/RusBEIR). Лицензия CC BY-SA 4.0.

- `docs.tsv` — `docid \t текст`, 15 010 абзацев: все 2 710 релевантных + 12 300 случайных остальных;
- `queries.tsv` — `qid \t dev|test \t текст`, 1 692 вопроса (400 dev, 1 292 test);
- `qrels.tsv` — `qid \t docid`, 2 845 оценок (все релевантные, бинарная релевантность).

Пересобрать данные: скачать из репозитория `data/corpus.jsonl.zip` (распаковать), `data/queries.jsonl`,
`data/test.jsonl` в папку `rubq/` и запустить `python prepare_data.py rubq`. Seed зафиксирован, результат детерминирован.

## Запуск

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook tfidf_seminar.ipynb
```

Весь ноутбук исполняется примерно за 4 минуты (Python 3.12). Самые долгие ячейки — оценка трёх формул whoosh (~75 сек).
`whoosh` 2.7.4 на Python 3.12 работает, но при первом импорте печатает `SyntaxWarning` — в ноутбуке они подавлены.
