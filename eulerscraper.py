#!/usr/bin/env python
import os
from bs4 import BeautifulSoup
from urllib import request
import sys
import json

with open('languages.json') as f:
    LANGUAGES = json.load(f)

LEGAL_CHARS = 'abcdefghijklmnopqrstuvwxyz01234567890_-'

LAST_PROB = 562

URL_ROOT = 'http://projecteuler.net/problem={}'

out_path, language = sys.argv[1:]

# out_path = 'tst'
# language = 'javascript'

ext, comment = LANGUAGES[language]

os.makedirs(out_path, exist_ok=True)

for i in range(1, LAST_PROB + 1):
    url = URL_ROOT.format(i)

    soup = BeautifulSoup(request.urlopen(url).read().decode())

    title = soup.find_all('h2')[0].text
    file_title = ''.join(char for char in '_'.join(title.split()).lower() if char in LEGAL_CHARS)

    filepath = os.path.join(out_path, '{:03}-{}{}'.format(i, file_title, ext))

    content = soup.find_all('div', {'class': 'problem_content'})[0]

    lines = [line for line in content.text.split('\n') if line]

    comment_text = ['{} {}'.format(comment, line) for line in [title.upper(), url] + lines]

    if os.path.exists(filepath):
        usr_input = input('WARNING: {} already exists. Overwrite? [y]/n: ')
        if usr_input == 'n':
            continue

    with open(filepath, 'w') as f:
        f.write('\n'.join(comment_text))
