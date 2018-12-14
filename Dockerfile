FROM centos
COPY bin/make_files.sh /
RUN yum -y makecache && \
    yum install -y epel-release && \
    yum makecache && \
    yum install -y python-pip
RUN pip install archive-manager
RUN mkdir -p /backup/backups-1 && \
    mkdir -p /backup/backups-2 && \
    mkdir -p /etc/archive-manager
COPY config.yml.example /etc/archive-manager/config.yml
RUN /make_files.sh
CMD /usr/bin/archive-manager