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

DIRECTORY = "../data/"
TRAIN = 'train.fr'
VALIDATE = 'validate.fr'
TEST = 'test.fr'

def insert_space(s):
    r = random.randint(1, len(s)-1)
    return s[:r] + ' ' + s[r:]

def insert_spaces(s):
    for i in range(random.randrange(len(s))):
        s = insert_space(s)
    return s

def corruptor(filename):
    i = 0
    lines = open(filename).read().splitlines()
    with open(filename, 'w') as out:
        for line in tqdm(lines, unit=' line'):
            corrupt = line.replace(" ", "") #Remove all space to maximize spacing error
            if i%20 != 0 and corrupt.strip() != '':
                corrupt = insert_spaces(corrupt) #Insert random spacing for 80% of the lines
            i += 1
            out.write(corrupt+'\n')

print('Inserting spacing errors for ' + DIRECTORY + TRAIN)
corruptor(DIRECTORY + TRAIN)
print('Inserting spacing errors for ' + DIRECTORY + VALIDATE)
corruptor(DIRECTORY + VALIDATE)
print('Inserting spacing errors for ' + DIRECTORY + TEST)
corruptor(DIRECTORY + TEST)