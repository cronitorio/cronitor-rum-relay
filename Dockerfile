ARG PYTHON_VERSION=3.11

# Fat image with compilers
FROM python:${PYTHON_VERSION} AS build

ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update -y

WORKDIR /opt/app/

RUN python -m venv /opt/venv/
RUN pip install -U pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Lightweight runtime image
FROM python:${PYTHON_VERSION}-slim as runtime

WORKDIR /opt/app/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y

COPY --from=build /opt/venv/ /opt/venv/

COPY . .

EXPOSE 8000
STOPSIGNAL SIGQUIT

CMD ["./bin/start.sh"]
