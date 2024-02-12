from typing import Dict
from collections import defaultdict
import re

not_tokens = ['are', 'is', 'a', 'the', 'am', 'at', 'of', 'and', 'in', 'on', 'or', 'but', 'by', 'to']

metadata = {
    'CC': 'координирующая конъюнкция',
    'CD': 'цифра',
    'DT': 'определитель',
    'MD': 'модальный глагол',
    'IN': "предлог/подчинительный союз",
    'JJ': "прилагательное",
    'JJR': "прилагательное сравнительное",
    'JJS': 'прилагательное в превосходной ',
    'NN': 'существительное в единственном числе',
    'NNS': 'существительное во множественном числе',
    'NNP': 'имя собственное в единственном числе',
    'NNPS': 'имя собственное, множественное число',
    'PRP': 'местоимение',
    'PRP$': 'местоимение',
    'RB': 'наречие',
    'RBR': 'наречие в сравнительной степени',
    'RBS': 'наречие в превосходной степени',
    'RP': 'частица',
    'UH': 'междометие',
    'VB': 'глагол, базовая форма',
    'VBD': 'глагол, прошедшее время',
    'VBG': 'глагол, герундий/причастие настоящего времени',
    'VBN': 'глагол, причастие прошедшего времени',
    'VBP': 'глагол, петь. настоящее, не трехмерное действие',
    'VBZ': 'глагол, поющий в 3-м лице. настоящее принимает',
    'WDT': 'вопрос, который',
    'WP': 'вопрос кто, что',
    'WRB': 'вопрос, где, когда'
}


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


def main(text: str):
    words = dict(sorted(parse_text(text=text).items(), key=lambda x: x[0]))

    return words
