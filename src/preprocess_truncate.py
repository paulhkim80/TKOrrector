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

import random
import fileinput
import sys
from tqdm import tqdm
from textwrap import wrap

DIRECTORY = "../data/"
TRAIN = 'train'
VALIDATE = 'validate'
TEST = 'test'

def truncate_line(s, size=80):
    if len(wrap(s, size)) > 0:
        return wrap(s, size)[0]
    else:
        return ''

def truncate_lines(filename):
    i = 0
    lines = open(filename).read().splitlines()
    with open(filename, 'w') as out:
        for line in tqdm(lines, unit=' line'):
            truncated = truncate_line(line)
            i += 1
            out.write(truncated+'\n')

print('Truncating lines' + DIRECTORY + TRAIN + '.fr')
truncate_lines(DIRECTORY + TRAIN + '.fr')
print('Truncating lines' + DIRECTORY + TRAIN + '.en')
truncate_lines(DIRECTORY + TRAIN + '.en')
print('Truncating lines' + DIRECTORY + VALIDATE + '.fr')
truncate_lines(DIRECTORY + VALIDATE + '.fr')
print('Truncating lines' + DIRECTORY + VALIDATE + '.en')
truncate_lines(DIRECTORY + VALIDATE + '.en')
print('Truncating lines' + DIRECTORY + TEST + '.fr')
truncate_lines(DIRECTORY + TEST + '.fr')
print('Truncating lines' + DIRECTORY + TEST + '.en')
truncate_lines(DIRECTORY + TEST + '.en')