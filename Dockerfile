FROM python:3.12-slim-trixie

WORKDIR /hunsum_search

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY main.py .

RUN pip install elasticsearch datasets
RUN pip install "fastapi[standard]"
RUN pip install "pytest"
RUN pip install "pydantic"

COPY start.sh /start.sh
COPY /adapters/ ./adapters/
COPY routers/ ./routers/
COPY schemas/ ./schemas/
RUN chmod +x /start.sh

CMD ["/start.sh"]
#CMD ["fastapi", "run", "routers/router.py", "--proxy-headers", "--port", "80"]