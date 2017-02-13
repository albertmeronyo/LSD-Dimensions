FROM python:2.7
MAINTAINER albert.merono@vu.nl

ENV LSD_USER="lsd" \
    LSD_HOME="/home/lsd" \
    LSD_LOG_DIR="/var/log/lsd" \
    GITLAB_VERSION=8.10.4 \
    LSD_CACHE_DIR="/etc/docker-lsd"

ENV LSD_INSTALL_DIR="${LSD_HOME}/lsd" \
    LSD_DATA_DIR="${LSD_HOME}/data" \
    LSD_BUILD_DIR="${LSD_CACHE_DIR}/build" \
    LSD_RUNTIME_DIR="${LSD_CACHE_DIR}/runtime"

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y nginx git-core logrotate python-pip locales gettext-base sudo \
 && update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX \
 && locale-gen en_US.UTF-8 \
 && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales \
 && rm -rf /var/lib/apt/lists/*

COPY assets/build/ ${LSD_BUILD_DIR}/
RUN bash ${LSD_BUILD_DIR}/install.sh

COPY assets/runtime/ ${LSD_RUNTIME_DIR}/
COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

EXPOSE 80/tcp

VOLUME ["${LSD_DATA_DIR}", "${LSD_LOG_DIR}"]
WORKDIR ${LSD_INSTALL_DIR}
ENTRYPOINT ["/sbin/entrypoint.sh"]
CMD ["app:start"]
