ARG VERSION
FROM ubuntu:${VERSION}
ARG VERSION

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

#
# Setup bash as the default shell.
#

RUN true \
    && unlink /bin/sh \
    && link /bin/bash /bin/sh \
    ;

#
# Configure apt for versions that reached EOL.
#

RUN if false \
        || [[ ${VERSION} == "19.10" ]] \
        || [[ ${VERSION} == "21.10" ]] \
    ; then \
        sed 's/http:\/\/archive.ubuntu.com\/ubuntu/http:\/\/old-releases.ubuntu.com\/ubuntu/' /etc/apt/sources.list > /etc/apt/sources.list1; \
        mv /etc/apt/sources.list1 /etc/apt/sources.list; \
        sed 's/http:\/\/security.ubuntu.com\/ubuntu/http:\/\/old-releases.ubuntu.com\/ubuntu/' /etc/apt/sources.list > /etc/apt/sources.list1; \
        mv /etc/apt/sources.list1 /etc/apt/sources.list; \
        sed 's/http:\/\/archive.canonical.com\/ubuntu/http:\/\/old-releases.ubuntu.com\/ubuntu/' /etc/apt/sources.list > /etc/apt/sources.list1; \
        mv /etc/apt/sources.list1 /etc/apt/sources.list; \
        sed 's/http:\/\/ports.ubuntu.com\/ubuntu-ports/http:\/\/old-releases.ubuntu.com\/ubuntu/' /etc/apt/sources.list > /etc/apt/sources.list1; \
        mv /etc/apt/sources.list1 /etc/apt/sources.list; \
    fi;

#
# Configure locale.
#

RUN true \
    && apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install locales \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    ;

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

#
# Install globally:
#  * python3
#  * python3-venv
#

RUN apt-get -y install \
    python3 \
    python3-venv \
    ;

#
# Create and configure the generic user
#

# Create and switch to the user.
ENV HOME=/home/user
RUN true \
    && groupadd -r -g 1234 user \
    && useradd -md ${HOME} -s /bin/bash -u 1234 -g 1234 user \
    && echo -e '# Add custom commands below' >> ${HOME}/.bashrc \
    ;
USER user

# Install Python packages for the user.
ENV PIP_CACHE_DIR=${HOME}/venv/.cache
RUN true \
    && python3 -m venv ${HOME}/venv \
    && source ${HOME}/venv/bin/activate \
    && python3 -m pip install pytest \
    && python3 -m pip install argapp==0.7.2 \
    ;
