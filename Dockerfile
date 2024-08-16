FROM python:3.10

# set env variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  CODE_DIR=/code

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR $CODE_DIR

COPY . $CODE_DIR/

WORKDIR $CODE_DIR/