#!/bin/bash

if [ ! -f model/corrector/dict.en.txt ] && [ ! -f model/corrector/dict.fr.txt ] && [ -f data/bin/dict.en.txt ] && [ -f data/bin/dict.fr.txt ]; then
    cp data/bin/dict.en.txt model/corrector/dict.en.txt
    cp data/bin/dict.en.txt model/corrector/dict.fr.txt
fi

cat | python src/tokenizer.py -mode interactive -unit jaso \
    | fairseq-interactive model/corrector \
      --path model/corrector/checkpoint_best.pt \
      --source-lang fr --target-lang en --beam 10 \
     | python src/format_fairseq_output.py 

