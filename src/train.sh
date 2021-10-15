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

DATA_FOLDER=../data/
MODEL_FOLER=../model/
MODEL=corrector
LOGS=logs

if [ ! -d ../$LOGS ]; then
    mkdir ../$LOGS
fi

if [ -d $DATA_FOLDER/bin/ ]; then
    rm -rf $DATA_FOLDER/bin/
fi

fairseq-preprocess --source-lang fr --target-lang en \
    --trainpref $DATA_FOLDER/train.tok \
    --validpref $DATA_FOLDER/validate.tok \
    --testpref $DATA_FOLDER/test.tok \
    --destdir $DATA_FOLDER/bin \
    --workers 10 \
    --memory-efficient-fp16

fairseq-train \
    $DATA_FOLDER/bin \
    --arch transformer \
    --encoder-layers 6 --decoder-layers 6 \
    --encoder-embed-dim 1024 --decoder-embed-dim 1024 \
    --encoder-ffn-embed-dim 4096 --decoder-ffn-embed-dim 4096 \
    --encoder-attention-heads 16 --decoder-attention-heads 16 \
    --share-decoder-input-output-embed \
    --optimizer adam --adam-betas '(0.9, 0.997)' --adam-eps 1e-09 --clip-norm 25.0 \
    --lr 1e-4 --lr-scheduler inverse_sqrt --warmup-updates 16000 \
    --dropout 0.1 --attention-dropout 0.1 --activation-dropout 0.1 \
    --weight-decay 0.00025 \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.2 \
    --max-tokens 1024 \
    --skip-invalid-size-inputs-valid-test \
    --save-dir $MODEL_FOLER$MODEL \
    --log-format json --log-interval 10 \
    --max-epoch 20 \
    --memory-efficient-fp16 \
    --model-parallel-size 1 \
    --batch-size 8 \
    --log-file ../$LOGS/$MODEL-01.log 
    
#    --dataset-impl lazy \