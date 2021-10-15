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
import argparse
import datetime
from tqdm import tqdm
from hangul_utils import join_jamos

def detokenize_line(s):
    # De-tokenize to calculate at the Korean character level istead of grapheme level
    tokens = s.split(' ')
    text = ''.join(tokens)
    text = join_jamos(text)
    text = text.replace('▁', ' ')
    text = text.replace('#', ' ')
    return text

def detokenize_lines(filename):
    lines = open(filename).read().splitlines()
    with open(filename, 'w') as out:
        for line in tqdm(lines, unit=' line'):
            if (len(line) > 0):
                text = detokenize_line(line)
                out.write(text+'\n')
            
def calculate_by_char(predicted, reference, metrics):
    predicted_next = iter(predicted)
    reference_next = iter(reference)
    predicted_char = next(predicted_next, '-1')
    reference_char = next(reference_next, '-1')
    
    for i in range(len(predicted) ):    

        if (predicted_char == '-1' or reference_char == '-1'):
            break

        if (predicted_char == reference_char): 
            if (predicted_char == ' '):
                metrics['tp'] += 1
            else:
                metrics['tn'] += 1
            
            predicted_char = next(predicted_next, '-1')
            reference_char = next(reference_next, '-1')
        else:
            if (predicted_char == ' '):
                metrics['fp'] += 1
                predicted_char = next(predicted_next, '-1')
            else:
                metrics['fn'] += 1
                reference_char = next(reference_next, '-1')
                
    
def calculate(predicted_filename, reference_filename):
    # Metric definition
    # TP = predicted, reference both contain space
    # TN = predicted, reference both do not contain space - *not counted since we don't use it for Precision, Recall, or F1 calculation
    # FP = only predicted contains space, reference do not contain space
    # FN = only predicted do not contain space, reference contain space
    # Mismatch is defined as when bad spacing sentence and good spacing sentence does not have identical string after trimming spaces and it indicates either insufficient training or training data.
    
    mismatch_count =0
    metrics = {'tp' : 0, 'tn': 0, 'fp' : 0, 'fn' : 0}
    
    predicted_lines = open(predicted_filename).read().splitlines()
    reference_lines = open(reference_filename).read().splitlines()
    reference_next = iter(reference_lines)
    
    mismatch_file = open("/tmp/mismatch.txt", "w") 
    performancedetail_file = open("/tmp/performancedetail.txt", "w")
    
    for predicted_line in tqdm(predicted_lines, unit=' line'): 
        reference_line = next(reference_next)
        
        reference_line = detokenize_line(reference_line)
        predicted_line = detokenize_line(predicted_line)
        
        predicted = predicted_line.replace(" ", "")
        reference = reference_line.replace(" ", "")
        if (predicted != reference):
            mismatch_count += 1
            mismatch_file.write("Predicted: {}\nReference: {}\n\n".format(predicted_line, reference_line))
        else:
            if (len(predicted + reference) > 0): # check if empty line
                if (predicted_line == reference_line):
                    metrics['tp'] += predicted_line.count(' ')
                    metrics['tn'] += len(predicted)
                else:
                    performancedetail_file.write("Predicted: {}\nReference: {}\n\n".format(predicted_line, reference_line))
                    calculate_by_char(predicted_line, reference_line, metrics)
    
    mismatch_file.close()
    performancedetail_file.close()
        
    precision = metrics['tp'] / (metrics['tp'] + metrics['fp'])
    recall = metrics['tp'] / (metrics['tp'] + metrics['fn'])
    f1 = metrics['tp'] / (metrics['tp'] + (1 / 2 * (metrics['fp'] + metrics['fn'])))
    performance = {'precision' : precision, 'recall' : recall, 'f1' : f1}
    with open('../performance.txt', 'w') as out:
        out.write('Performance measure date and time: {}\n'.format(str(datetime.datetime.now())))
        out.write(str(performance) + '\n')
    print(performance)
    print("Mismatch: {}".format(mismatch_count))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-predicted_path', required=True)
    parser.add_argument('-reference_path', required=True)
    args = parser.parse_args()
    
    calculate(args.predicted_path, args.reference_path)
    