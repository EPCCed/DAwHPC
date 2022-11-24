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
RUN rm -rf /tmp/DAwHPC && rm -rf work && rm -rf temp && rm -rf DAwHPC

# clone repo
RUN git clone https://github.com/EPCCed/DAwHPC.git

# Practical 1 - intro (no data files)
RUN mv DAwHPC/Practical1.ipynb temp

# Practical 2 - DataCleaning
RUN mv DAwHPC/Practical2a.ipynb temp && \
    mv DAwHPC/Practical2b.ipynb temp && \
    mkdir -p temp/DatasetsForPracticals/DataCleaning && \
    mv DAwHPC/DatasetsForPracticals/DataCleaning/somedata.csv temp/DatasetsForPracticals/DataCleaning && \
    mv DAwHPC/DatasetsForPracticals/DataCleaning/daltons.txt temp/DatasetsForPracticals/DataCleaning

# Practical 3 - DataCleaning with Dask (will not run on EIDF this year (22/23))

# Practical 4 - Linear Regression
#RUN mv DAwHPC/Practical4.ipynb temp # not in repo yet!
RUN mkdir -p temp/DatasetsForPracticals/LinearRegression && \
    mv DAwHPC/DatasetsForPracticals/LinearRegression/mtcars.csv temp/DatasetsForPracticals/LinearRegression && \
    mv DAwHPC/DatasetsForPracticals/LinearRegression/tortoise.csv temp/DatasetsForPracticals/LinearRegression

# Practical 5 - NaiveBayes
#RUN mv DAwHPC/Practical5.ipynb temp # not in repo yet!
#RUN mkdir -p temp/DatasetsForPracticals/NaiveBayes && \
#    mv DAwHPC/DatasetsForPracticals/NaiveBayes/adult_data.csv temp/DatasetsForPracticals/NaiveBayes && \
#    mv DAwHPC/DatasetsForPracticals/NaiveBayes/adult_test.csv temp/DatasetsForPracticals/NaiveBayes

# Practical 6 - Decision trees and forests in sklearn
#RUN mv DAwHPC/Practical6.ipynb temp # not in repo yet!
RUN mkdir -p temp/DatasetsForPracticals/DecisionTreesAndForests && \
    mv DAwHPC/DatasetsForPracticals/DecisionTreesAndForests/carseats.csv temp/DatasetsForPracticals/DecisionTreesAndForests

# Practical 7 - kmeans sklearn and hard coded
#RUN mv DAwHPC/Practical7.ipynb temp # not in repo yet!

# Practical 8 - NeuralNetworks in sklearn
#RUN mv DAwHPC/Practical8.ipynb temp # not in repo yet!
RUN mkdir -p temp/DatasetsForPracticals/NeuralNetworks/simple_sklearn && \
    mv DAwHPC/DatasetsForPracticals/NeuralNetworks/simple_sklearn/data.txt temp/DatasetsForPracticals/NeuralNetworks/simple_sklearn && \
    mv DAwHPC/DatasetsForPracticals/NeuralNetworks/simple_sklearn/empty.txt temp/DatasetsForPracticals/NeuralNetworks/simple_sklearn

# Practical 9 - NeuralNetworks in PyTorch (will not run on EIDF this year (22/23))

# Practical 10 - SPARK/pySPARK (will not run on EIDF this year (22/23))

#remove repo and replace with temp
RUN rm -rf DAwHPC && mv temp /tmp/DAwHPC

CMD jupyter lab --ip=0.0.0.0 --port=8888 --NotebookApp.token=
