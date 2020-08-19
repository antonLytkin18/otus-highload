FROM centos:7

ENV container docker

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

VOLUME [ "/sys/fs/cgroup" ]

RUN yum update -y && yum -y install sudo git ncurses-devel make cmake gcc gcc-c++ boost boost-devel wget unzip nano bzip2 mysql-devel mysql-lib

RUN git clone https://github.com/tarantool/mysql-tarantool-replication.git
RUN cd mysql-tarantool-replication && \
    git submodule update --init --recursive

RUN cd mysql-tarantool-replication && \
    cmake . && \
    make && \
    cp replicatord /usr/local/sbin/replicatord

COPY conf/replicatord.service /etc/systemd/system
COPY conf/replicatord.yml /usr/local/etc/replicatord.yml

RUN systemctl enable replicatord.service

CMD ["/usr/sbin/init"]