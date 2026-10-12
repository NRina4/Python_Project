# Воспроизводимый конвейер P3: данные -> результат -> сайт.
# Использование:
#   make figures  - пересобрать график из data/experiment.csv (с кэшированием)
#   make build    - figures + метка версии + строгая сборка сайта
#   make serve    - локальный предпросмотр

figures:
	python scripts/generate_results.py

build: figures
	python scripts/stamp_version.py
	mkdocs build --strict

serve:
	mkdocs serve
