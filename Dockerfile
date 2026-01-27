FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY main.py .

RUN pip install elasticsearch datasets

CMD ["python", "main.py"]