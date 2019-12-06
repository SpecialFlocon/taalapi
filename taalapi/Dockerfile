# Build stage
FROM python:3

RUN groupadd -g 500 taalapi && \
    useradd -d /home/taalapi -g taalapi -m -N -u 500 taalapi

USER taalapi

RUN python3 -m venv /home/taalapi/venv
COPY requirements.txt .

ENV PATH "/home/taalapi/venv/bin:$PATH"
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3-slim

RUN groupadd -g 500 taalapi && \
    useradd -d /home/taalapi -g taalapi -m -N -u 500 taalapi && \
    mkdir -p /srv/taalapi /var/run/taalapi && \
    chown taalapi:taalapi /srv/taalapi /var/run/taalapi
RUN apt-get -y update && \
    apt-get -y install apt-utils && \
    apt-get -y install libxml2

USER taalapi
WORKDIR /srv/taalapi

COPY --chown=taalapi:taalapi . .
COPY --chown=taalapi:taalapi run.sh /
COPY --from=0 /home/taalapi/venv /home/taalapi/venv

ENV PATH="/home/taalapi/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/home/taalapi/venv

CMD ["/run.sh"]
