from typing import Dict
from collections import defaultdict
import re


not_tokens = ['are', 'is', 'a', 'the', 'am', 'at', 'of', 'and', 'in', 'on', 'or', 'but', 'by', 'to']


def process_item(item: str) -> None | str:
    reg_exp = r'((?<![a-zA-Z])\.?\S\.)|[\‘\’\/\.\,:;!\?\"\(\)…\“\”]|\d+(-\d+)?|^[–\-]$'
    item = re.sub(reg_exp, '', item)

    return item


def parse_text(text: str) -> Dict[str, int]:
    parsed_text = defaultdict(lambda: 0)
    for i in text.split():
        i = process_item(i)
        if i not in not_tokens and i not in [j.capitalize() for j in not_tokens] and i.isalpha():
            parsed_text[i.lower()] += 1

    return parsed_text


def main():
    for i in range(1, 100):
        try:
            with open(f'test{i}.txt', 'r') as f:
                text = f.read()
            words = dict(sorted(parse_text(text=text).items(), key=lambda x: x[0]))
            for key, value in words.items():
                print("{0}: {1}".format(key, value))
        except FileNotFoundError:
            break
        print('=========================')


if __name__ == '__main__':
    main()
