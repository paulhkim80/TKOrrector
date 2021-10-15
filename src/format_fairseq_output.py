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

import re
import sys
from hangul_utils import join_jamos

def main():
    prev_line_no = None
    for line in sys.stdin:
        line = line[:-1]
        match = re.match(r'^H-(\d+)', line)
        if not match:
            continue
        tokens = line.split('\t')[2].split(' ')
        text = ''.join(tokens)
        text = join_jamos(text)
        line_no = int(match.group(1))
        assert not prev_line_no or line_no == prev_line_no + 1
        prev_line_no = line_no
        text = text.replace('▁', ' ')
        text = text.replace('#', ' ')
        print(text)

if __name__ == '__main__':
    main()