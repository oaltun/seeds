FROM python:3.10-bookworm



RUN mkdir /app
WORKDIR /app
RUN python3 -m venv venv

COPY image/requirements.txt ./
RUN /app/venv/bin/python3 -m pip install --no-cache-dir -r requirements.txt

COPY ./image /app/image

# for reuse of running container
COPY loop.py ./

WORKDIR /app/image

RUN git init
RUN git config user.name "gpt-3.5-turbo"
RUN git config user.email "gpt-3.5-turbo@razalt.com"
RUN git branch -m master main
RUN git add --all
RUN git commit -m "init"

