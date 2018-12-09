FROM centos
COPY dist/*.noarch.rpm /
COPY bin/make_files.sh /
RUN yum install python-yaml -y
RUN rpm -ivh /*.rpm
RUN mkdir -p /backup/backups-1
RUN mkdir -p /backup/backups-2
RUN cp /etc/archive-manager/config.yml.example /etc/archive-manager/config.yml
CMD /usr/bin/archive-manager