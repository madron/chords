FROM chordpro/chordpro:v6.020.0

# Required packages
RUN apt update \
    && apt install -y python3 python3-pip python3-poetry python3-psycopg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install dependencies
COPY pyproject.toml poetry.lock /src/
RUN poetry config virtualenvs.create false
RUN poetry install
