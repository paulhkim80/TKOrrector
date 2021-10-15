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

FOLDER=../data/
CLEAN_TRAIN=train.en
CLEAN_VALIDATE=validate.en
CLEAN_TEST=test.en
CORRUPT_TRAIN=train.fr
CORRUPT_VALIDATE=validate.fr
CORRUPT_TEST=test.fr

cp $FOLDER$CLEAN_TRAIN $FOLDER$CORRUPT_TRAIN
cp $FOLDER$CLEAN_VALIDATE $FOLDER$CORRUPT_VALIDATE
cp $FOLDER$CLEAN_TEST $FOLDER$CORRUPT_TEST

python preprocess_corruptor.py