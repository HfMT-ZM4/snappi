FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    bash \
    bc \
    binutils \
    build-essential \
    bzip2 \
    cpio \
    g++ \
    gcc \
    git \
    gzip \
    locales \
    libncurses5-dev \
    libdevmapper-dev \
    libsystemd-dev \
    make \
    mercurial \
    whois \
    patch \
    perl \
    python3 \
    rsync \
    sed \
    file \
    tar \
    vim \ 
    unzip \
    wget \
    bison \
    flex \
    cmake \
    libssl-dev \
    libfdt-dev \
    ts-node \
    npm

RUN locale-gen en_US.utf8

RUN useradd --user-group --create-home --home-dir /build --no-log-init --shell /bin/bash builder

RUN mkdir /buildroot
RUN chown builder:builder /buildroot

USER builder

RUN git clone git://git.buildroot.net/buildroot --depth=1 --branch=2024.08 /buildroot

WORKDIR /build

RUN ["/bin/bash"]
