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

# Run batch translation job with test dataset.
fairseq-generate ../data/bin  \
    --path ../model/corrector/checkpoint_best.pt \
    --beam 10 --batch-size 128 --remove-bpe | tee /tmp/gen.out

# Extract translated text
grep ^H /tmp/gen.out | cut -f3-  > /tmp/predicted
# Extract original, training reference text
grep ^T /tmp/gen.out | cut -f2-  > /tmp/reference

# Calculate performance metrics
python ./calculate_metrics.py -predicted_path=/tmp/predicted -reference_path=/tmp/reference