# Информационный поиск и ранжирование

Материалы курса «Информационный поиск и ранжирование», НИУ ВШЭ, осень 2026.

Преподаватель: Руслан Аллаяров.

## Что здесь лежит

| Папка | Что внутри |
|---|---|
| `homeworks/` | шаблоны и описания домашних заданий |
| `seminars/` | ноутбуки и данные семинаров (появляются после занятия) |

Домашние задания:

| ДЗ | Тема | Дедлайн |
|---|---|---|
| [ДЗ 1](homeworks/hw1-boolean-retrieval/) | Индексация и булев поиск | 10.10.2026 |
| [ДЗ 2](homeworks/hw2-text-ranking/) | Текстовое ранжирование | 04.11.2026 |

Семинары:

| № | Тема | Папка |
|---|---|---|
| 2 | Индексация и булев поиск, whoosh | [seminars/02-indexing-whoosh](seminars/02-indexing-whoosh/) |
| 4 | Текстовое ранжирование, часть I: TF-IDF, морфология, LSA | [seminars/04-text-ranking-tfidf](seminars/04-text-ranking-tfidf/) |
| 5 | Текстовое ранжирование, часть II: BM25, BM25F, языковые модели, nDCG | [seminars/05-text-ranking-bm25](seminars/05-text-ranking-bm25/) |

## Как запускать код

Нужна машина с Linux или macOS и Python 3.10+ (проверяем на 3.12).

Для каждого ДЗ заводите **отдельное** виртуальное окружение и ставьте в него только то, что нужно для этого ДЗ:

```bash
# из корня склонированного репозитория
mkdir -p .venvs
python3 -m venv .venvs/hw1-boolean-retrieval
source .venvs/hw1-boolean-retrieval/bin/activate
pip install -r homeworks/hw1-boolean-retrieval/requirements.txt
```

Когда решение готово, зафиксируйте окружение:

```bash
pip freeze > requirements.txt
```

Проверяющий восстановит ровно это окружение командой `pip install -r requirements.txt` и запустит ваше решение в нём.

## Вопросы

Пишите в чат курса.
