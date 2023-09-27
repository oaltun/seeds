FROM python:3.10-bookworm





WORKDIR /app/env1
RUN python3 -m venv venv
COPY initial_software/requirements.txt ./
RUN /app/env1/venv/bin/python3 -m pip install --no-cache-dir -r requirements.txt



RUN cp -r /app/env1 /app/env2


WORKDIR /app
COPY loop.py ./
