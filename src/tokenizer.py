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

import sys
import re
import argparse
from tqdm import tqdm
from hangul_utils import split_syllables, join_jamos

CHO = (
    u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)
JOONG = (
    u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ',
    u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ', u'ㅣ'
)
JONG = (
    u'', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ',
    u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)
JAMO = CHO + JOONG + JONG[1:]
ALL_CHARS = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,!?'-")
ALL_CHARS = tuple(ALL_CHARS) + JAMO

def clean(s):
    s = s.strip()
    s = ''.join(ch if ch in ALL_CHARS else '#' for ch in s)
    s = re.sub(' +', ' ', s).strip()
    return s

def to_jaso(s):
    return clean(split_syllables(s))

def tokenize_by_eojeol_char(s):
    return s.split(' ')    

def tokenize_by_eojeol_jaso(s):
    text = [to_jaso(token) for token in tokenize_by_eojeol_char(s)]
    #Flatten list
    flat_list = []
    for sublist in text:
        for item in sublist:
            flat_list.append(item)
        flat_list.append('▁')
    text = flat_list[:-1]
    return text

def get_tokenizer(unit):
    return getattr(sys.modules[__name__], 'tokenize_by_eojeol_{}'.format(unit))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', choices=['batch', 'interactive'], required=True)
    parser.add_argument('-unit', choices=['jaso', 'char'], required=True)
    parser.add_argument('-input_path')
    parser.add_argument('-output_path')
    args = parser.parse_args()
    
    tokenizer = get_tokenizer(args.unit)
    if args.mode == 'batch':  
        lines = open(args.input_path).read().splitlines()
        with open(args.output_path, 'w') as out:
            for line in tqdm(lines, unit=' line'):
                tokens = line[:-1]
                tokens = tokenizer(tokens)
                out.write(' '.join(tokens) + '\n')
    else:
        for line in sys.stdin:
            tokens = line[:-1]
            tokens = tokenizer(tokens)
            print(' '.join(tokens))