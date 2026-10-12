# Отчёт по заданию 3

## 1. Ход работы

1. Установлен Python 3.14.4, проверены `pip` и `virtualenv`, создано окружение `.venv/`.
2. Зависимости зафиксированы в `my-project/requirements.txt` точными версиями; кэш и сборка исключены через `.gitignore` (`venv`, `site/`, `_build/`, `.cache`).
3. Установлен MkDocs + Material, создан каркас сайта (`my-project/docs/`, `my-project/mkdocs.yml`).
4. Локальная проверка: `mkdocs serve` для предпросмотра, `mkdocs build --strict` для сборки.
5. Репозиторий инициализирован и отправлен на GitHub (`NRina4/Python_Project`, ветка `master`).
6. Настроен GitHub Actions (см. раздел 4), в `Settings → Pages → Source` выбрано `GitHub Actions`.
7. Использована официальная связка `upload-pages-artifact + deploy-pages` (разница со способом `push в gh-pages` — в разделе 4).
8. Отечественный хостинг: <!-- TODO: Helios, аккаунт/сервер, URL -->.
9. `site_url` задан через `!ENV [SITE_URL, ...]` (`my-project/mkdocs.yml:3`), `use_directory_urls: true`; для Helios-подкаталога `SITE_URL` переопределяется в workflow.
10. Проверка деплоя: HTTP-код, контрольная строка в HTML, поиск, формулы при недоступном CDN (см. раздел 6).
11. Лицензии: код — MIT (`LICENSE-CODE-MIT` в корне репозитория), контент — CC BY 4.0 (`LICENSE-CONTENT-CC-BY-4.0` в корне); упоминание на главной странице.
12. Отладка зафиксирована в разделе 7.

## 2. Теоретическое задание Т1

Выполнен сравнительный анализ четырёх генераторов: MkDocs + Material, Sphinx + MyST-Parser, Pelican, Jupyter Book 2.
Полный текст: [Анализ генераторов](research.md).

Итоговые взвешенные баллы (шкала 0–5, веса в сумме 100%):

| Генератор | Балл из 100 |
|---|---:|
| Sphinx + MyST-Parser | 93,8 |
| Jupyter Book 2 | 77,4 |
| MkDocs + Material | 72,0 |
| Pelican | 54,6 |

Вывод: по совокупности научных критериев оптимален Sphinx + MyST-Parser; для реализации конвейера в данной работе выбран MkDocs + Material (простота, быстрая сборка, русский поиск, работа в подкаталоге). Условия смены вывода — в `research.md`, раздел 9.

## 3. Практическое задание P3

Конвейер «данные → результат → сайт»:

```text
my-project/data/experiment.csv → scripts/generate_results.py → docs/assets/result.png → mkdocs build → сайт
```

Результат: [Эксперимент](experiment.md). Исходные данные меняются → `generate_results.py` пересчитывает график → push запускает CI → сайт обновляется.

Кэширование: повторный запуск без изменения `experiment.csv` пропускает пересчёт (`skip: up to date`).
Замер локально (Windows, Python 3.14.4): полный пересчёт после удаления `result.png` — 1,90 с; повтор с актуальным png — 1,46 с.
Выигрыш ~0,44 с (~23%); основное время в обоих случаях — старт интерпретатора и импорт matplotlib/pandas, на больших данных выигрыш будет больше.

Метка версии выводится внизу страницы эксперимента (`scripts/stamp_version.py` в CI перед сборкой): коммит, дата сборки UTC, md5 `experiment.csv`.

## 4. Пайплайны

### 4.1. GitHub Pages (использован)

Workflow `.github/workflows/gh-pages.yml` (шаги прокомментированы в файле):
`checkout → setup-python 3.14 → pip install -r my-project/requirements.txt → generate_results.py → mkdocs build --strict (SITE_URL=https://nrina4.github.io/Python_Project/) → upload-pages-artifact (my-project/site) → deploy-pages`.

### 4.2. Push в `gh-pages` (peaceiris, не использован — для сравнения)

Готовый HTML коммитится ботом в отдельную ветку `gh-pages`, Pages отдаёт её (`Source = Deploy from a branch`). Плюсы: простота на старых репо. Минусы: мусорная ветка сборок, нужны права `contents: write`, конфликты при параллельных пушах. Официальный способ вместо ветки использует артефакт и OIDC (`pages: write, id-token: write`), поэтому выбран он.

### 4.3. Helios (Static HTML)

<!-- TODO: YAML workflow под Helios, SITE_URL подкаталога -->

## 5. Ссылки

- Репозиторий: `https://github.com/NRina4/Python_Project`
- GitHub Pages: `https://nrina4.github.io/Python_Project/`
- Отечественный хостинг: <!-- TODO: URL Helios -->

## 6. Измерения (только таблицами)

| Замер | Значение |
|---|---|
| Время `mkdocs build --strict` локально (Windows) | 0,62 с |
| Время `mkdocs build --strict` (лог Actions) | TODO (после финального пуша) |
| Размер `my-project/site` | 3 255 309 Б (≈ 3,10 MiB) |
| Размер `docs/assets/result.png` | 30 878 Б (≈ 30,2 KiB) |
| Размер `docs/assets/actions-success.png` | 185 072 Б (≈ 180,7 KiB) |
| Размер `docs/assets/pages-site.png` | 202 325 Б (≈ 197,6 KiB) |
| Длительность jobs build / deploy (Actions) | TODO (после финального пуша) |
| Время холодной/инкрементальной сборки 4 генераторов | см. `research.md`, раздел 4 |
| Стоимость Plotly (до/после) | см. `research.md`, раздел 6 |

Скриншоты: зелёный запуск Actions — `assets/actions-success.png` (готов); главная Pages — `assets/pages-site.png` (готов); проваленный запуск — TODO (взять со страницы красного run); Helios и демо P3 — после финального пуша.

![Зелёный запуск Actions](assets/actions-success.png)

![Главная страница на GitHub Pages](assets/pages-site.png)

## 7. Отладка

### Ошибка 1. Deploy 404 — Pages не включён
- Текст: `Failed to create deployment (status: 404) ... Ensure GitHub Pages has been enabled`.
- Гипотеза: `deploy-pages` некуда публиковать, `Source` не переключён на Actions.
- Проверка: открыли `settings/pages`, артефакт в логе при этом найден (`artifact_id ...`).
- Решение: `Settings → Pages → Source = GitHub Actions`, затем `Re-run failed jobs`. Повторный запуск зелёный.

### Ошибка 2. <!-- TODO -->
- Текст: TODO. Гипотеза: TODO. Проверка: TODO. Решение: TODO.

### Ошибка 3. <!-- TODO -->
- Текст: TODO. Гипотеза: TODO. Проверка: TODO. Решение: TODO.

## 8. Вывод

Рекомендуемый стек для публикации результатов в данной предметной области: Sphinx + MyST-Parser для полного научного аппарата; MkDocs + Material — при приоритете простоты и публикации уже посчитанных результатов отдельным pipeline (реализовано здесь); Jupyter Book 2 — при исполняемых ноутбуках в сборке; Pelican — для контентных сайтов без научной типографики. Ограничения, меняющие рекомендацию, — в `research.md`, раздел 9.
