FROM python:3.10 

ENV SHELL /bin/bash
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

# Environment Setting
RUN apt update

# install packages
RUN apt install -y vim zip unzip tree graphviz fonts-noto-cjk

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# remove font
RUN rm -r /usr/share/fonts/truetype \
    && fc-cache -fv

# install python packages
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# install gcloud CLI
RUN curl https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
# RUN gcloud config set project $PROJECT_ID