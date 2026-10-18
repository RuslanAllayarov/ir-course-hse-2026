# Семинар: текстовое ранжирование, часть II

Ноутбук `bm25_seminar.ipynb`:
- метрики MAP и nDCG, проблема неразмеченных документов;
- BM25 руками и подбор k1, b;
- сверка с `bm25s`;
- зоны и BM25F;
- языковые модели (Дирихле, Елинек — Мерсер);
- близость слов;
- BM25F в whoosh;
- значимость различий: парный t-тест и перестановочный тест;
- задания.

## Данные

Подвыборка русской части MIRACL (Zhang et al., «MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages», TACL 2023):
- запросы и оценки: https://huggingface.co/datasets/miracl/miracl (dev, 1252 запроса);
- корпус: https://huggingface.co/datasets/miracl/miracl-corpus (пассажи русской Википедии с заголовками).

Лицензия: Apache-2.0.

В подвыборку вошли все 12 607 размеченных пассажей (релевантные и размеченные нерелевантные) и 8 105 случайных, итого 20 712.

| Файл | Формат |
|---|---|
| `docs.tsv` | `docid \t title \t text` |
| `queries.tsv` | `qid \t dev|test \t текст` (400 dev для подбора параметров, 852 test) |
| `qrels.tsv` | `qid \t docid \t rel` (1 — релевантен, 0 — размечен как нерелевантный) |

Пересобрать данные: `python prepare_data.py`. Скрипт читает корпус (~2 ГБ gz) потоком и работает около 6 минут. Результат детерминирован.

## Запуск

```
pip install -r requirements.txt
jupyter notebook bm25_seminar.ipynb
```

Полный прогон ноутбука — около 2.5 минут. Индекс whoosh создаётся в `indexdir_bm25` и удаляется последней ячейкой.
