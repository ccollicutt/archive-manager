FROM python:3.6-alpine
ARG version
COPY bin/make_files.sh /
RUN pip install archive-manager==$version
RUN mkdir -p /backup/backups-1 && \
    mkdir -p /backup/backups-2 && \
    mkdir -p /etc/archive-manager
COPY config.yml.example /etc/archive-manager/config.yml
RUN /make_files.sh
CMD /usr/bin/archive-manager