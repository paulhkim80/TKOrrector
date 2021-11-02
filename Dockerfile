# Copyright 2021 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG BASE_IMAGE=nvidia/cuda:11.4.2-runtime-ubuntu20.04

# Pretrained model file names are: small, medium, large, xlarge
ARG MODEL_FILE=large

FROM $BASE_IMAGE as base

# Non-GPU Enabled: demo.sh, GPU Enabled: demo_realtime.sh
ENV STARTUP_CMD demo_realtime.sh

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo java-common wget git make gcc g++ \
    python3.9 python3-pip python-is-python3 tzdata apt-utils autoconf automake  && \
    wget https://corretto.aws/downloads/latest/amazon-corretto-8-x64-linux-jdk.deb && \
    dpkg -i amazon-corretto-8-x64-linux-jdk.deb && \
    pip3 install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 \
    -f https://download.pytorch.org/whl/cu113/torch_stable.html && \
    git clone https://github.com/paulhkim80/hangul-utils.git && \
    git clone https://github.com/paulhkim80/TKOrrector.git && \
    git clone https://github.com/pytorch/fairseq.git

WORKDIR /hangul-utils
RUN bash install_mecab_ko.sh && \
    bash install_twkorean.sh && \
    python setup.py install

WORKDIR /fairseq
RUN pip3 install --editable ./

WORKDIR /TKOrrector
RUN wget https://storage.googleapis.com/paulsandbox_asia/TKOrrector/TKOrrector_$MODEL_FILE.tar.gz && \
    tar zxvf TKOrrector_$MODEL_FILE.tar.gz && \
    touch data/bin/train.fr-en.en.idx

CMD bash $STARTUP_CMD