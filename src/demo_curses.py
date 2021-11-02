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
import curses
import locale
locale.setlocale(locale.LC_ALL, '')

CHECKPOINT_DIR = '../model/corrector/'
CHECKPOINT_FILE = 'checkpoint_best.pt'

ss = ""

corrector = TransformerModel.from_pretrained(
    CHECKPOINT_DIR,
    CHECKPOINT_FILE,
    '../../data/bin/'
)

# Move model to GPU for faster translation
corrector.cuda()

tokenizer = get_tokenizer('jaso')

def translate(inStr):
    # Calls for an infinite loop that keeps executing
    # until an exception occurs
    inTokens = tokenizer(inStr) 
    outTokens = corrector.translate(' '.join(inTokens))
    outstr = detokenize_line(str(outTokens))

    return outstr

def init(screen):
    # Clear and refresh the screen for a blank canvas
    screen.clear()
    screen.refresh()

    screen.addstr(0, 0, u"수정한 문장 입니다: \n")
    screen.addstr(3, 0, u"띄어쓰기를 고칠 문장을 입력하세요: \n")

    global ss
    ss = ""

def draw(screen):

    init(screen)

    global ss
    ss = ""
    while True:
        s = screen.get_wch()

        if isinstance(s, int) == True: # If the first character is deleted
            init(screen)
            continue
        elif ord(s) == 10: # If the enter key is entered
            init(screen)
        else:
            ss += s
            screen.addstr(1, 0, translate(ss), curses.A_BOLD)
        
        screen.addstr(4, 0, ss, curses.A_BOLD)

        # Refresh the screen
        screen.refresh()

def main():
    curses.wrapper(draw)

if __name__ == "__main__":
    main()