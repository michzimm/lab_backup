FROM python:3.9-slim

ARG password=password
ENV PASSWD=$password

RUN mkdir /lab_backup
RUN mkdir /lab_backup/config_backups

COPY ./lab_backup.py /lab_backup/
COPY ./requirements.txt /lab_backup/

RUN pip install -r /lab_backup/requirements.txt


WORKDIR /lab_backup

ENTRYPOINT ["/bin/bash", "-c", "python3 lab_backup.py"]