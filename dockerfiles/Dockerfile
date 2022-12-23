FROM ubuntu:focal
ARG NJOBS=6
LABEL org.opencontainers.image.title="ROFT Samples Docker Image"
LABEL org.opencontainers.image.description="Infrastructure for running ROFT samples"
LABEL org.opencontainers.image.source="https://raw.githubusercontent.com/hsp-iit/roft-samples/master/dockerfiles/Dockerfile"
LABEL org.opencontainers.image.authors="Nicola A. Piga <nicola.piga@iit.it>"

# Use /bin/bash instead of /bin/sh
SHELL ["/bin/bash", "-c"]

# Non-interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Set the locale
RUN apt update && \
    apt install -y -qq locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Install essentials
RUN apt update && \
    apt install --no-install-recommends -y -qq apt-utils build-essential ca-certificates cmake cmake-curses-gui curl emacs-nox git glmark2 gnupg2 htop iputils-ping jq libssl-dev libusb-1.0-0-dev lsb-release mesa-utils nano psmisc python3-virtualenv sudo unzip vim wget zip && \
    rm -rf /var/lib/apt/lists/*

# Install GitHub cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt update && \
    apt install --no-install-recommends -y -qq gh && \
    rm -rf /var/lib/apt/lists/*

# Install additional dependencies
RUN apt update && \
    apt install --no-install-recommends -y -qq eog libassimp-dev libconfig++-dev libglfw3-dev libglew-dev libgtk2.0-dev libglm-dev libeigen3-dev libpython3-dev libqt5svg5 libtclap-dev libvtk7-dev && \
    git clone --progress https://github.com/robotology/robotology-superbuild && cd robotology-superbuild && bash scripts/install_apt_dependencies.sh && \
    rm -rf /var/lib/apt/lists/*

# Build robotology-superbuild
RUN git config --global user.name "user" && \
    git config --global user.email "user@email.com" && \
    cd robotology-superbuild && \
    git checkout v2022.11.0 && \
    mkdir build && cd build && \
    cmake -DROBOTOLOGY_ENABLE_CORE=ON -DROBOTOLOGY_USES_GAZEBO=OFF -DROBOTOLOGY_USES_PYTHON=ON -DROBOTOLOGY_USES_LUA=ON -DYCM_EP_ADDITIONAL_CMAKE_ARGS:STRING="-DICUB_COMPILE_BINDINGS:BOOL=ON -DCREATE_PYTHON:BOOL=ON -DENABLE_yarpmod_RGBDSensorWrapper:BOOL=ON -DENABLE_yarpmod_RGBDSensorClient:BOOL=ON -DENABLE_yarpcar_mjpeg:BOOL=ON -DENABLE_yarppm_depthimage_to_rgb:BOOL=ON -DENABLE_yarppm_depthimage_compression_zlib:BOOL=ON" ../ && \
    make -j$NJOBS

# Create user with passwordless sudo
RUN useradd -l -G sudo -md /home/user -s /bin/bash -p user user && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers

# Switch to user
USER user

# Configure emacs
RUN echo "(setq-default indent-tabs-mode nil)" >> /home/user/.emacs.el && \
    echo "(setq-default tab-width 4)" >> /home/user/.emacs.el && \
    echo "(setq make-backup-files nil)" >> /home/user/.emacs.el && \
    echo "(setq auto-save-default nil)" >> /home/user/.emacs.el && \
    echo "(setq c-default-style \"linux\"" >> /home/user/.emacs.el && \
    echo "      c-basic-offset 4)" >> /home/user/.emacs.el && \
    echo "(global-subword-mode 1)" >> /home/user/.emacs.el && \
    echo "(add-hook 'before-save-hook 'delete-trailing-whitespace)" >> /home/user/.emacs.el && \
    echo "(custom-set-variables '(custom-enabled-themes '(tango-dark)))" >> /home/user/.emacs.el && \
    echo "(custom-set-faces)" >> /home/user/.emacs.elx

# Configure robotology-superbuild
RUN echo "source /robotology-superbuild/build/install/share/robotology-superbuild/setup.sh" >> /home/user/.bashrc

# Launch bash from /home/user
WORKDIR /home/user
CMD ["bash"]
