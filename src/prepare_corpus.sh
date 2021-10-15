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

CORPUS1=NIKL_NEWSPAPER_2020_v1.1
CORPUS2=NIKL_WRITTEN_v1.0
FOLDERS=( $CORPUS1 $CORPUS2 )
OUTPUT=corpus
OUTPUT_TRAIN=train
OUTPUT_VALIDATE=validate
OUTPUT_TEST=test

if [ -f ../data/$OUTPUT ]; then
    rm ../data/$OUTPUT
fi
touch ../data/$OUTPUT

get_corpus () {
    i=0
    # for FILE in ./{$CORPUS1,$CORPUS2}/*; do
    for FILE in $1; do
        #Skip pdf manual (ieterated first due to broken korean filename)
        if [ $i -eq 0 ]; then
            ((i++))
            continue
        fi
        echo "Processing $FILE"
        # Replace quotes and forward slashes as the new articles contain alot of them and spacing training don't require them. Also, split long paragraphs into separate lines to decrease the parameter dimensions as Korean spacing don't need to take paragraph context into account, only per sentence.
        jq '.document[].paragraph[].form' $FILE | sed -e 's/\"//g' -e 's/\\//g' -e "s/\'//g" -e "s/\.$/.\n/g" >> ../data/$OUTPUT
        ((i++))
        echo "Total number of files processed: $(($i - 1))"
        if [ $2 -gt 0 ] && [ $i -eq $2 ]; then
            break
        fi
    done
}

# Include every text from newspaper corpus
get_corpus "../data/$CORPUS1/*" 5
# Limit to 10 files from written corpus as it contains too much text to gain any value 
# from training all of them as they are pretty similar
get_corpus "../data/$CORPUS2/*" 10

#Remove empty lines
sed -i '/^$/d' ../data/$OUTPUT
# head -n 10000 ../data/$OUTPUT > ../data/$OUTPUT.tmp
# mv ../data/$OUTPUT.tmp ../data/$OUTPUT

if [ -f ../data/$OUTPUT_TRAIN.en ]; then
    rm ../data/$OUTPUT_TRAIN.en
fi
if [ -f ../data/$OUTPUT_VALIDATE.en ]; then
    rm ../data/$OUTPUT_VALIDATE.en
fi
if [ -f ../data/$OUTPUT_TEST.en ]; then
    rm ../data/$OUTPUT_TEST.en
fi

# Split 80% of the corpus as training and 20% to dev to be split equally again into 10% validation adn 10% test sets
shuf ../data/$OUTPUT | split -a1 -d -l $(( $(wc -l <../data/$OUTPUT) * 80 / 100 )) - ../data/output

mv ../data/output0 ../data/$OUTPUT_TRAIN.en
cp ../data/$OUTPUT_TRAIN.en ../data/$OUTPUT_TRAIN.fr

mv ../data/output1 ../data/$OUTPUT_VALIDATE.en
split -a1 -d -l $(( ($(wc -l <../data/$OUTPUT_VALIDATE.en) + 1) / 2 )) <../data/$OUTPUT_VALIDATE.en - ../data/output
mv ../data/output0 ../data/$OUTPUT_VALIDATE.en
cp ../data/$OUTPUT_VALIDATE.en ../data/$OUTPUT_VALIDATE.fr
mv ../data/output1 ../data/$OUTPUT_TEST.en
cp ../data/$OUTPUT_TEST.en ../data/$OUTPUT_TEST.fr

bash ./preprocess_truncate.sh
bash ./preprocess_corruptor.sh