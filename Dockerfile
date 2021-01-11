FROM python:3.8-slim

ENV HOME /opt/app
RUN mkdir $HOME
WORKDIR $HOME

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]