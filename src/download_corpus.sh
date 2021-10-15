#!/bin/bash

# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

mkdir ../data

rm -rf ../data/NIKL_NEWSPAPER_2020_v1.1
rm -rf ../data/NIKL_WRITTEN_v1.0

mkdir ../data/NIKL_NEWSPAPER_2020_v1.1
mkdir ../data/NIKL_WRITTEN_v1.0

gsutil -m cp gs://[todo: Replace with your location for NIKL_NEWSPAPER_2020_v1.1.zip] ../data/
gsutil -m cp gs://[todo: Replace with your location for NIKL_WRITTEN\(v1.0\).zip] ../data/

unzip -j -d ../data/NIKL_NEWSPAPER_2020_v1.1 ../data/NIKL_NEWSPAPER_2020_v1.1.zip
unzip -j -d ../data/NIKL_WRITTEN_v1.0 ../data/NIKL_WRITTEN\(v1.0\).zip