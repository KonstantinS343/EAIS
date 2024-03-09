from nltk.corpus import movie_reviews
import nltk

import json
from typing import Dict, Union

from metadata import metadata


def prepare() -> Dict[str, Dict[str, Union[str, int]]]:
    corpus = dict()
    frequency = nltk.FreqDist(movie_reviews.words())
    for key, value in frequency.items():
        try:
            corpus[key] = {
                    "frequency": value,
                    "additional information": metadata[nltk.pos_tag([key])[0][1]],
                }
        except KeyError:
            continue

    with open('movie_corpus.json', 'w') as file:
        json.dump(corpus, file, indent=4, ensure_ascii=False)

    return corpus
