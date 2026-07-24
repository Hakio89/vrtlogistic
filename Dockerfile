# --- Etap 1: Budowanie i instalacja zależności ---
FROM python:3.12-slim-bookworm AS builder

# Instalujemy uv z oficjalnego obrazu
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Narzędzia potrzebne do skompilowania mysqlclient oraz biblioteki ODBC
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Ustawiamy katalog roboczy
WORKDIR /vrtlogistic

# Pobieramy Tailwind CLI v4 dopasowany do architektury
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then BINARY="tailwindcss-linux-x64"; \
    elif [ "$arch" = "aarch64" ]; then BINARY="tailwindcss-linux-arm64"; \
    else echo "Unsupported architecture: $arch" && exit 1; fi && \
    curl -L "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/${BINARY}" -o /usr/local/bin/tailwindcss && \
    chmod +x /usr/local/bin/tailwindcss

# Optymalizacja warstw: Kopiujemy tylko pliki definicji paczek
COPY pyproject.toml uv.lock ./

# Instalujemy zależności (bez samej aplikacji jeszcze)
# --frozen: gwarantuje użycie wersji z uv.lock
# --no-install-project: nie instalujemy jeszcze kodu źródłowego
RUN uv sync --frozen --no-install-project --no-dev

# Kopiujemy kod i generujemy CSS w etapie builder
COPY . .
RUN tailwindcss -i ./vrtlogistic/static/css/input.css -o ./vrtlogistic/static/css/vrtlogistic.css --minify && \
    rm ./vrtlogistic/static/css/input.css


# --- Etap 2: Finalny obraz uruchomieniowy ---
FROM python:3.12-slim-bookworm

WORKDIR /vrtlogistic

# Biblioteki dla MySQL oraz unixodbc
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    pkg-config \
    curl \
    gnupg2 \
    unixodbc \
    && rm -rf /var/lib/apt/lists/*

# Instalacja Microsoft ODBC Driver 18 dla SQL Server (wymagany przez pyodbc)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

#1. TWORZYMY UŻYTKOWNIKA I GRUPĘ
# -m: tworzy katalog domowy
# -u 1000: dopasowanie do standardowego ID użytkownika na Linuxie (ułatwia uprawnienia)
RUN groupadd -g 1000 django-group && \
    useradd -u 1000 -g django-group -m django-user && \
    chown django-user:django-group /vrtlogistic

# Kopiujemy binarne uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Kopiujemy całą aplikację (z gotowym CSS) oraz venv z buildera
COPY --from=builder --chown=django-user:django-group /vrtlogistic /vrtlogistic

# Dodajemy venv do PATH, aby móc używać zainstalowanych paczek bezpośrednio
ENV PATH="/vrtlogistic/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown django-user:django-group /entrypoint.sh

# 3. PRZEŁĄCZAMY SIĘ NA NOWEGO UŻYTKOWNIKA
USER django-user
ENTRYPOINT ["/entrypoint.sh"]