# syntax=docker/dockerfile:1
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app/ /app/app/
# no extra deps needed
CMD ["python", "app/hello.py"]
