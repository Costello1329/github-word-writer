from datetime import date, timedelta, datetime
from random import choice, randint
from termcolor import cprint
import urllib.request
import subprocess
import shutil
import string
import math
import uuid
import sys
import os
import re

from alphabet import alphabet


# UTILS
def get_id():
    return str(uuid.uuid4()).split('-')[0]


# GRAPHICS

def letter_width(letter):
    return 0 if len(letter) == 0 else max([max(row) if len(row) else 0 for row in letter]) + 1


def get_coordinates_for_word(word):
    width = 52
    height = 7
    space_width = 1

    letter_widths = [letter_width(alphabet[letter]) for letter in word]
    word_width = sum(letter_widths) + space_width * (len(word) - 1)
    x_border = (width - word_width) // 2

    if x_border < 0:
        raise Exception('word is too wide: {}'.format(word_width))

    coordinates = []
    for i in range(0, len(word)):
        letter_shift_x = x_border + sum(letter_widths[0:i]) + space_width * i
        letter_height = len(alphabet[word[i]])
        letter_shift_y = math.ceil((height - letter_height) / 2)

        if letter_shift_y < 0:
            raise Exception('letter is too high: {}'.format(letter_height))

        for dy in range(0, letter_height):
            for dx in alphabet[word[i]][dy]:
                coordinates.append((letter_shift_x + dx, letter_shift_y + dy))
    return coordinates


# GIT HELPERS

def init_repo(origin, username, email):
    repo = 'repo-{}'.format(get_id())
    branch_name = 'branch-{}'.format(get_id())
    os.mkdir(repo)
    subprocess.call((
        'cd {} && git init -b {} 2>&1 >/dev/null && ' +
        'git config user.name "{}" && git config user.email "{}" && ' +
        'git remote add origin {}'
    ).format(repo, branch_name, username, email, origin), shell=True)
    return repo, branch_name


def make_commit_on_date(repo, date, density):
    for r in range(density):
        date = '{} {}:{}:{}'.format(str(date), randint(9, 15), randint(0, 59), randint(0, 59))
        subprocess.call((
            'cd {} && echo "{}" >> {} && git add . && git commit -m "{}" 2>&1 >/dev/null &&' +
            'GIT_COMMITTER_DATE="{}" git commit --amend --no-edit --date="{}" 2>&1 >/dev/null'
        ).format(repo, get_id(), repo + '.txt', get_id(), date, date), shell=True)


def push_repo(repo, branch_name):
    subprocess.call(
        'cd {} && git push -u origin {} 2>&1 >/dev/null && cd ../ && rm -rf {}'.format(repo, branch_name, repo), shell=True)


# MAIN PROCEDURE

def check_word(word):
    if not all([letter in alphabet for letter in word]):
        raise Exception('Unsupported letter')


def get_dates_pixels(username):
    response = urllib.request.urlopen('https://github.com/{}'.format(username))
    html_doc = str(response.read())

    r = r'data-count="([0-9]*)" data-date="(\d\d\d\d)-(\d\d)-(\d\d)"'
    matches = [(int(el) for el in t) for t in re.findall(r, html_doc)]
    return [(datetime(y, m, d), int(v)) for v, y, m, d in matches]


def write_word(word, origin, username, email):
    check_word(word)

    cprint('Initializing repo ...', 'green')
    repo, branch_name = init_repo(origin, username, email)

    cprint('Normalizing ...', 'green')
    dates_pixels = get_dates_pixels(username)
    dates, pixels = zip(*dates_pixels)
    max_pixel = sorted(pixels, reverse=True)[0]
    cprint('Max value: {}'.format(max_pixel), 'blue')
    
    dates_pixels_dict = dict(dates_pixels)

    cprint('Making commits ...', 'green')

    for date in dates:
        make_commit_on_date(repo, date, max_pixel - dates_pixels_dict[date])
    
    coords = get_coordinates_for_word(word)

    for x, y in coords:
        date = dates[7 * x + y]
        # 3 is the optimal constant to make the word data-level equal to 4
        make_commit_on_date(repo, date, max(3 * max_pixel, 1))

    cprint('Pushing commits ...', 'green')
    push_repo(repo, branch_name)


def main():
    origin = ''
    username = ''
    email = ''

    if len(sys.argv) > 2:
        cprint('Using unparsed args', 'yellow')
        _, origin, username, email = sys.argv

    else:
        print('Input origin (repo url): ', end='')
        origin = input().strip()
        print('Input gh username: ', end='')
        username = input().strip()
        print('Input gh email: ', end='')
        email = input().strip()

    print('Input word: ', end='')
    word = input().strip()

    try:
        write_word(word, origin, username, email)
    except Exception as ex:
        cprint(str(ex), 'red')


if __name__ == '__main__':
    main()
