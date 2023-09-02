FROM chordpro/chordpro:v6.020.0

# Required packages
RUN apt update \
    && apt install -y gosu nginx python3 python3-pip python3-poetry uwsgi-plugin-python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install dependencies
COPY pyproject.toml poetry.lock /src/
RUN poetry config virtualenvs.create false
RUN poetry install --without test

ENV DJANGO_SETTINGS_MODULE=settings.docker
ENV PYTHONUNBUFFERED=1

# Source
COPY . /src
RUN    chmod 755 /src/manage.py \
    && chmod 755 /src/docker/entrypoint.sh \
    && sync \
    && /src/manage.py collectstatic --link --noinput --verbosity=0

WORKDIR /src/
VOLUME ["/var/tmp/nginx"]

EXPOSE 8000

ENTRYPOINT ["/src/docker/entrypoint.sh"]
CMD ["uwsgi", "--plugins", "/usr/lib/uwsgi/plugins/python311_plugin.so", "--master", "--processes", "4", "--threads", "8", "--chdir", "/src", "--wsgi", "settings.wsgi", "--http-socket", ":8000", "--stats", ":9191"]
