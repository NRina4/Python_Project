# Python_Project — публикация результатов экспериментов через SSG

Учебный проект по заданию 3: генератор статических сайтов на Python + CI/CD + деплой на GitHub Pages и Helios.

## Структура

```text
.
├── my-project/            # основной сайт (MkDocs + Material) — то, что деплоится
│   ├── data/experiment.csv
│   ├── scripts/generate_results.py
│   ├── docs/              # index.md, research.md (T1), experiment.md (P3)
│   ├── mkdocs.yml
│   └── requirements.txt   # точные пины
├── T1-benchmark/          # стенды для сравнения 4 генераторов (замеры для T1)
│   ├── mkdocs-test/ sphinx-test/ pelican-test/ jupyterbook-test/
│   ├── plotly_graph.py / plotly_graph.html
│   └── sizes_before.txt
├── .venv/                 # виртуальное окружение (Windows, Python 3.14.4)
└── .gitignore
```

`my-project/README.md` — описание основного сайта. Этот файл — как работать со всем репозиторием.

## Требования

- Python 3.14.4, `pip`, `virtualenv`.
- Окружение уже создано в `.venv/`. Пересоздать при необходимости:
  `python -m virtualenv .venv`

## Быстрый старт (Windows)

```bat
.venv\Scripts\activate
pip install -r my-project\requirements.txt
python my-project\scripts\generate_results.py
.venv\Scripts\python.exe -m mkdocs serve -f my-project\mkdocs.yml
```

Открыть `http://127.0.0.1:8000/`.

Linux (то же окружение не подойдёт, создать своё):

```bash
python3 -m venv .venv-linux && source .venv-linux/bin/activate
pip install -r my-project/requirements.txt
python my-project/scripts/generate_results.py
mkdocs serve -f my-project/mkdocs.yml
```

## Работа с основным сайтом

```bat
REM пересобрать график из данных
python my-project\scripts\generate_results.py

REM предпросмотр
.venv\Scripts\python.exe -m mkdocs serve -f my-project\mkdocs.yml

REM строгая сборка (как в CI, битые ссылки = ошибка)
.venv\Scripts\python.exe -m mkdocs build --strict -f my-project\mkdocs.yml
```

Результат — `my-project/site/` (в git не коммитится).

Смена базового URL (подкаталог Helios vs корень Pages):

```bat
set SITE_URL=https://<helios>/~login/lab3/ && .venv\Scripts\python.exe -m mkdocs build --strict -f my-project\mkdocs.yml
```

По умолчанию `SITE_URL=http://localhost:8000/` (см. `my-project/mkdocs.yml:3`).

## Конвейер P3 «данные → результат → сайт»

```text
my-project/data/experiment.csv → scripts/generate_results.py → docs/assets/result.png → mkdocs build → site/
```

Поменял `experiment.csv` → запусти `generate_results.py` → проверь `serve` → коммить. В CI те же шаги выполняются автоматически.

## Стенды T1-benchmark

Одинаковая тестовая страница собирается четырьмя генераторами для таблиц в `research.md` (время холодной/инкрементальной сборки, вес результата, русский поиск, стоимость Plotly). Каждый подкаталог собирается своими средствами (см. конфиги внутри), в общий сайт они не входят.

## Деплой

- GitHub Pages: workflow `my-project/.github/workflows/gh-pages.yml` (`upload-pages-artifact` + `deploy-pages`), в настройках репо `Pages → Source = GitHub Actions`.
- Helios: отдельный workflow под экшен «Static HTML» с `SITE_URL` подкаталога.
- Проверка после деплоя: HTTP 200, контрольная строка в HTML, поиск, формулы при заблокированном CDN.

## Частые ошибки

- `No module named mkdocs` — не активирован `.venv` или вызывается системный python.
- `build --strict` красный — читать первое `WARNING`, обычно нет картинки/ссылки.
- Сайт работает на Pages, ломается на Helios — абсолютные ссылки `/assets/...` вместо относительных, не задан `SITE_URL` подкаталога.
- Формулы не рендерятся — нет `docs/javascripts/mathjax.js` или заблокирован `unpkg.com` (см. `mkdocs.yml:34-36`).
