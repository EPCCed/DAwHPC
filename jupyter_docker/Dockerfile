ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/datascience-notebook
FROM $BASE_CONTAINER

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER ${NB_UID}

USER root

WORKDIR "/"

ENV TERM=xterm
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV TZ=Etc/UTC
ARG ORIG_PATH="${PATH}"
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${CONDA_DIR}/bin

# Start of future-kubernetes bits
# kubectl is only needed for monitoring/diagnostics.
RUN apt-get update && \
    apt-get install -y curl && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    cp kubectl /usr/local/bin

# End of future-kubernetes bits

# Start of Intro to ML with Python bits

USER ${NB_UID}

WORKDIR "/home/${NB_USER}"

# Install Tensorflow and other ML dependencies
# Python-graphviz required installation through conda/mamba so that required env vars are set properly when plotting with matplotlib
RUN arch=$(uname -m) && \
    if [ "${arch}" == "aarch64" ]; then \
        # Prevent libmamba from sporadically hanging on arm64 under QEMU
        # <https://github.com/mamba-org/mamba/issues/1611>
        export G_SLICE=always-malloc; \
    fi && \
    mamba install --quiet --yes \
    'numpy' \
    'pandas' \
    'matplotlib' \
    'tableone' \
    'scikit-learn' \
    'seaborn' \
    'keras' \
    'python-graphviz' \
    'statsmodels' \
    'jupyterlab' \
    'plotly' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# remove below bits for installation as a 'server option' launched through jhub itself
USER ${NB_UID}
# Switch back to jovyan to avoid accidental container runs as root

WORKDIR "${HOME}"
RUN rmdir work
RUN mkdir DAwHPC_practicals
RUN mkdir DAwHPC_data

# clone repo
RUN git clone https://github.com/EPCCed/DAwHPC.git

# Practical 1
RUN cp DAwHPC/Practical1.ipynb DAwHPC_practicals

# Practical 2
RUN cp DAwHPC/Practical2a.ipynb DAwHPC_practicals && \
    cp DAwHPC/Practical2b.ipynb DAwHPC_practicals && \
    cp DAwHPC/DatasetsForPracticals/DataCleaning/somedata.csv DAwHPC_data && \
    cp DAwHPC/DatasetsForPracticals/DataCleaning/daltons.txt DAwHPC_data

#remove repo
RUN rm -rf DAwHPC

CMD jupyter lab --ip=0.0.0.0 --port=8888 --NotebookApp.token=
