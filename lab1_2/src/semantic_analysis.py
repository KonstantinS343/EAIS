from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from nltk import word_tokenize

import string
from typing import List, Tuple, Dict
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


def get_synonyms_antonyms(
    word: str, words: List[Synset]
) -> Tuple[List[str], List[str]]:
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
            hyponyms.add(i.name().split(".")[0])
        for i in item.hypernyms():
            hypernyms.add(i.name().split(".")[0])

    return list(hyponyms), list(hypernyms)


def get_semantic_analysis_in_str(
    sentence: str, semantic_analysis: Dict[str, Dict[str, str | List[str]]]
) -> str:
    output = "<html>"
    for word, description in semantic_analysis.items():
        output += (
                "= " * ((40 - len(word.capitalize())) // 2)
                + f"<b>{word.capitalize()}</b>"
                + " =" * ((40 - len(word.capitalize())) // 2)
                + "<br>"
        )
        for arg, value in description.items():
            if isinstance(value, str):
                output += f"<b>{arg}:</b> " + f"{value}<br>"
            elif isinstance(value, list):
                output += (
                    f"<b>{arg}:</b> "
                    + f"{str(value).replace('[', '').replace(']', '')}<br>"
                )
        output += "= " * 40 + "<br><br></html>"

    return output


def semantic_anallysis(text: str) -> str:
    words = [
        word
        for word in word_tokenize(text)
        if word not in string.punctuation and word not in string.digits
    ]

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

        output_in_dict[word.capitalize()] = {
            "Defenition": defenition,
            "Example": example,
            "Synonyms": synonyms,
            "Antonyms": antonyms,
            "Hyponyms": hyponyms,
            "Hypernyms": hypernyms,
        }
    output = get_semantic_analysis_in_str(
        sentence=text, semantic_analysis=output_in_dict
    )
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
