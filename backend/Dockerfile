FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip install cryptography

COPY . .

# ensure wait script is executable and install netcat for port checks
RUN apt-get update \
	&& apt-get install -y --no-install-recommends netcat-openbsd \
	&& rm -rf /var/lib/apt/lists/*
RUN chmod +x wait-for-it.sh || true

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

