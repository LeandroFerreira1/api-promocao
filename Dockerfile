FROM python:3.10

WORKDIR /code

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./api_promo/ /code/api_promo/

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

RUN python api_promo/criar_tabelas.py

CMD ["uvicorn", "api_promo.main:app", "--host", "0.0.0.0", "--port", "8000"]
