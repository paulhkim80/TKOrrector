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

ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:21.09-py3

FROM $BASE_IMAGE as base

RUN apt-get update && \
    apt-get install sudo java-common && \
    wget https://corretto.aws/downloads/latest/amazon-corretto-8-x64-linux-jdk.deb && \
    dpkg -i amazon-corretto-8-x64-linux-jdk.deb && \
    git clone https://github.com/paulhkim80/hangul-utils.git && \
    git clone https://github.com/paulhkim80/TKOrrector.git && \
    git clone https://github.com/pytorch/fairseq.git 

WORKDIR /workspace/hangul-utils
RUN bash install_mecab_ko.sh && \
    bash install_twkorean.sh && \
    python setup.py install

WORKDIR /workspace/fairseq
RUN pip3 install --editable ./

WORKDIR /workspace/TKOrrector
RUN wget https://storage.googleapis.com/paulsandbox_asia/TKOrrector/TKOrrector.tar.gz && \
    tar zxvf TKOrrector.tar.gz 

CMD bash demo.sh