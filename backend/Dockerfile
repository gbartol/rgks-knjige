# Za razliku od frontend Dockerfilea, ovdje nemamo posebnu builder sliku.
# To je stoga što Python kod ne kompajliramo; na serveru pokrećemo izvorni kod backenda.

FROM python:3.12-slim

WORKDIR /app

# Nije nam potrebno virtualno okruženje jer je unutar Docker containera ovo jedina Python aplikacija.
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root

COPY . .
RUN python manage.py collectstatic --noinput

# Backend aplikacija neće biti javno dostupna, ali mora biti dostupna frontend aplikaciji.
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
