#!/usr/bin/env python
import os
from bs4 import BeautifulSoup
from urllib import request
import sys
import json
from threading import Thread
import queue
from warnings import warn

with open('languages.json') as f:
    LANGUAGES = json.load(f)

LEGAL_CHARS = 'abcdefghijklmnopqrstuvwxyz01234567890_-'
LAST_PROB = 562
URL_ROOT = 'http://projecteuler.net/problem={}'
THREADS = 10

out_path, language = sys.argv[1:]

# out_path = 'tst'
# language = 'javascript'

ext, comment = LANGUAGES[language]

print('Ensuring path exists: {}'.format(out_path))
os.makedirs(out_path, exist_ok=True)

def fetch_problem(num):
    print('Fetching problem {} of {}...'.format(num, LAST_PROB))
    url = URL_ROOT.format(num)

    soup = BeautifulSoup(request.urlopen(url).read().decode())

    title = soup.find_all('h2')[0].text
    file_title = ''.join(char for char in '_'.join(title.split()).lower() if char in LEGAL_CHARS)

    filepath = os.path.join(out_path, '{:03}-{}{}'.format(num, file_title, ext))

    content = soup.find_all('div', {'class': 'problem_content'})[0]

    lines = [line for line in content.text.split('\n') if line]

    comment_text = ['{} {}'.format(comment, line) for line in [title.upper(), url] + lines]

    if os.path.exists(filepath):
        warn('File {} already exists: skipping.'.format(filepath))
        return

    # print('\tSaving problem at {}'.format(filepath))

    with open(filepath, 'w') as f:
        f.write('\n'.join(comment_text))


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        fetch_problem(item)
        q.task_done()

q = queue.Queue()
threads = []
for i in range(THREADS):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(1, LAST_PROB+1):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for _ in range(THREADS):
    q.put(None)
for t in threads:
    t.join()
