help:
	@echo
	@echo "install                            -- install backend dependencies"
	@echo "lint                               -- lint backend"
	@echo "format                             -- format backend"
	@echo "mypy                               -- type check backend"
	@echo "translate                          -- start translator server"
	@echo "dev                                -- start backend development server"
	@echo


.PHONY: install
install:
	uv sync --frozen

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: mypy
mypy:
	MYPY_PATH=./,translator_service uv run mypy .

.PHONY: format
format:
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: translate
translate:
	cd translator_service && uv run uvicorn main:app --reload --host "127.0.0.1" --port 8081 --workers 1 --log-level info


.PHONY: dev
dev:
	uv run uvicorn main:app --reload --host "127.0.0.1" --port 8080 --workers 1 --log-level info