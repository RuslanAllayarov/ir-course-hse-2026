# Семинар 2. Индексация и булев поиск

Руками собираем обратный индекс, а потом смотрим, как то же самое устроено в поисковом движке `whoosh`.

| Файл | Что это |
|---|---|
| `indexing_whoosh.ipynb` | ноутбук семинара (с выводами) |
| `docs.tsv` | 2781 документ: `docid`, `title`, `body` через таб; леммы в верхнем регистре |
| `queries.numerate.txt` | 325 запросов: номер, таб, текст; `(A\|B)` — синонимы |
| `requirements.txt` | зависимости |

## Как запустить

```bash
# из корня репозитория
python3 -m venv .venvs/seminar-02
source .venvs/seminar-02/bin/activate
pip install -r seminars/02-indexing-whoosh/requirements.txt jupyter
cd seminars/02-indexing-whoosh
jupyter notebook indexing_whoosh.ipynb
```

Ноутбук ждёт `docs.tsv` и `queries.numerate.txt` в той же папке. Весь Run All занимает меньше минуты.

## Что внутри

1. Наивный поиск полным перебором и почему так нельзя.
2. Свой обратный индекс: постинг-листы, пересечение за один проход, И/ИЛИ-запросы. Это основа [ДЗ 1](../../homeworks/hw1-boolean-retrieval/).
3. Тот же поиск в `whoosh`: схема, индексация, словарь и постинги, парсер запросов, анализатор, мягкое ИЛИ.
4. Задания: ужать индекс через дельты в `array("i")`; найти и объяснить расхождения с whoosh.

## Откуда данные

`docs.tsv` собран из открытых трибанков Universal Dependencies:

- [UD_Russian-Taiga](https://github.com/UniversalDependencies/UD_Russian-Taiga) — CC BY-SA 4.0
- [UD_Russian-SynTagRus](https://github.com/UniversalDependencies/UD_Russian-SynTagRus) — CC BY-NC-SA 4.0
- [UD_Russian-GSD](https://github.com/UniversalDependencies/UD_Russian-GSD) — CC BY-SA 4.0

Документ — отрезок подряд идущих предложений одного исходного текста, приведённых к леммам; `title` — первые 14 лемм документа. Запросы собраны из слов документов, синонимы — ручной словарь.

Файлы данных в этой папке распространяются по **CC BY-NC-SA 4.0** (из-за SynTagRus): только некоммерческое использование, с указанием источников. Код ноутбука — по лицензии MIT, как и весь репозиторий.
