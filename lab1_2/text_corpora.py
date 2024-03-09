import nltk
from nltk.corpus import stopwords

from typing import Dict, List, Union
import string
import os
import json

from prepare_corpus import prepare


def import_corpus() -> Dict[str, Dict[str, Union[str, int]]]:
    with open('movie_corpus.json', 'r') as file:
        corpus = json.load(file)

    return corpus


def find_words(words: List[str]) -> Dict[str, Dict[str, Union[str, int]]]:
    words_with_info = dict()
    if not os.path.isfile('./movie_corpus.json'):
        frequency = prepare()
    else:
        frequency = import_corpus()

    for i in words:
        try:
            if frequency[i]['frequency'] != 0:
                words_with_info[i] = frequency[i]
        except KeyError:
            continue

    return words_with_info


def main(text: str) -> Dict[str, Dict[str, Union[str, int]]]:
    parsed_text = list()
    stop_words = set(stopwords.words('english')).union(set(string.punctuation))

    for i in nltk.word_tokenize(text):
        if i not in stop_words:
            parsed_text.append(i)

    words_dict = find_words(words=parsed_text)
    return words_dict
