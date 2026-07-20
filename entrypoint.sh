#!/bin/bash
set -e

# Upewnij się, że używamy ustawień produkcyjnych
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-vrtlogistic.settings}

# Czekamy chwilę na bazę danych (opcjonalnie, depends_on w compose już to wspiera)
echo "Wykonywanie migracji bazy danych..."
uv run manage.py migrate --noinput

# Zbieranie plików statycznych (potrzebne na serwerze)
echo "Zbieranie plików statycznych..."
uv run manage.py collectstatic --noinput --clear

# Uruchomienie serwera (używamy gunicorna dla stabilności na serwerze)
echo "Uruchamianie serwera..."
exec uv run gunicorn vrtlogistic.wsgi:application --bind 0.0.0.0:8000