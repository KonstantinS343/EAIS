from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from nltk import word_tokenize

import string
from typing import List, Tuple
import logging
import time
import json


logging.basicConfig(
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    datefmt="%m.%d.%Y %H:%M:%S",
    level=logging.INFO,
)


def try_get_obj_by_name(word: str, words: List[Synset]) -> Synset:
    for i in words:
        if word.lower() in i._name:
            return i

    return words[0]


def get_synonyms_antonyms(word: str, words: List[Synset]) -> Tuple[List[str], List[str]]:
    synonyms = set()
    antonyms = set()

    for item in words:
        for i in item.lemmas():
            if word.lower() != i.name():
                synonyms.add(i.name())
            for j in i.antonyms():
                antonyms.add(j.name())

    return list(synonyms), list(antonyms)


def get_hyponyms_hypernyms(words: List[Synset]) -> Tuple[List[str], List[str]]:
    hyponyms = set()
    hypernyms = set()

    for item in words:
        for i in item.hyponyms():
            hyponyms.add(i.name().split('.')[0])
        for i in item.hypernyms():
            hypernyms.add(i.name().split('.')[0])

    return list(hyponyms), list(hypernyms)


def semantic_anallysis(text: str) -> str:
    words = [
        word
        for word in word_tokenize(text)
        if word not in string.punctuation and word not in string.digits
    ]
    output = "<html>"
    output_in_dict = {}
    start = time.time()

    for word in words:
        cursor: List[Synset] = wn.synsets(word)
        if not cursor:
            continue

        defenition = try_get_obj_by_name(word=word, words=cursor).definition()
        example = try_get_obj_by_name(word=word, words=cursor).examples()
        synonyms, antonyms = get_synonyms_antonyms(word=word, words=cursor)
        hyponyms, hypernyms = get_hyponyms_hypernyms(words=cursor)

        output += (
            "= " * ((40 - len(word.capitalize())) // 2)
            + f'<b>{word.capitalize()}</b>'
            + " =" * ((40 - len(word.capitalize())) // 2)
            + "<br>"
        )
        output += f"<b>{word.capitalize()}</b> - " + f"{defenition}<br>"
        output += "<b>Examples:</b> " + f"{str(example).replace('[', '').replace(']', '')}<br>"
        output += "<b>Synonyms:</b> " + f"{str(synonyms).replace('[', '').replace(']', '')}<br>"
        output += "<b>Antonyms:</b> " + f"{str(antonyms).replace('[', '').replace(']', '')}<br>"
        output += "<b>Hyponyms:</b> " + f"{str(hyponyms).replace('[', '').replace(']', '')}<br>"
        output += "<b>Hypernyms:</b> " + f"{str(hypernyms).replace('[', '').replace(']', '')}<br>"
        output += "= " * 40 + "<br><br></html>"

        output_in_dict[word.capitalize()] = {
            "Defenition": defenition,
            "Example": example,
            "Synonyms": synonyms,
            "Antonyms": antonyms,
            "Hyponyms": hyponyms,
            "Hypernyms": hypernyms
        }

    with open("semantic.json", "a+") as file:
        file.seek(0)

        try:
            dict_from_file = json.load(file)
        except Exception:
            dict_from_file = {}

        dict_from_file[text] = output_in_dict

        file.seek(0)
        file.truncate()

        json.dump(dict_from_file, file, indent=4)

    logging.info(time.time() - start)
    return output

