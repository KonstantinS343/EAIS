import nltk
from nltk.corpus import movie_reviews, stopwords

from typing import Dict, List
import string


def find_words(words: List[str]) -> Dict[str, int]:
    words_with_info = dict()
    frequency = nltk.FreqDist(movie_reviews.words())

    for i in words:
        if frequency[i] != 0:
            words_with_info[i] = frequency[i]

    return words_with_info


def main(text: str) -> Dict[str, int]:
    parsed_text = list()
    stop_words = set(stopwords.words('english')).union(set(string.punctuation))

    for i in nltk.word_tokenize(text):
        if i not in stop_words:
            parsed_text.append(i)

    words_dict = find_words(words=parsed_text)
    return words_dict
