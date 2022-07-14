FROM python:3.9-slim

RUN mkdir /lab_backup
RUN mkdir /lab_backup/config_backups

COPY ./lab_backup.py /lab_backup/
COPY ./requirements.txt /lab_backup/
COPY ./update_password.py /lab_backup/

RUN pip install -r /lab_backup/requirements.txt
RUN /lab_backup/update_password.py $passwd

WORKDIR /lab_backup

ENTRYPOINT ["./lab_backup.py"]