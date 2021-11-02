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

from fairseq.models.transformer import TransformerModel
from tokenizer import get_tokenizer
from calculate_metrics import detokenize_line

CHECKPOINT_DIR = '../model/corrector/'
CHECKPOINT_FILE = 'checkpoint_best.pt'


def translate():
    
    corrector = TransformerModel.from_pretrained(
        CHECKPOINT_DIR,
        CHECKPOINT_FILE,
        '../../data/bin/'
    )

    tokenizer = get_tokenizer('jaso')
    
    # Calls for an infinite loop that keeps executing
    # until an exception occurs
    while True:
        inStr = input("띄어쓰기를 고칠 문장을 입력하세요: \n")
        inTokens = tokenizer(inStr)
        outTokens = corrector.translate(' '.join(inTokens))
        outstr = detokenize_line(str(outTokens))
        
        print('\n수정한 문장 입니다:')
        print(outstr + '\n\n')

translate()