import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import xml.etree.ElementTree as ET
import xml.dom.minidom
import string
import os
import re

from lab1_2.conf.metadata import metadata


def text_to_xml(text: str, root_name: str) -> str:
    text = re.sub(r"[^\x20-\x7F]", "", text)
    root = ET.Element(root_name)

    sentences = sent_tokenize(text)

    stop_words = set(stopwords.words("english")).union(set(string.punctuation))

    for i, sentence in enumerate(sentences):
        sentence_element = ET.SubElement(root, "sentence", id=str(i + 1))

        words = word_tokenize(sentence)

        for j, word in enumerate(words):
            if word not in stop_words:
                try:
                    word_element = ET.SubElement(
                        sentence_element,
                        "word",
                        id=str(j + 1),
                        info=metadata[nltk.pos_tag([word])[0][1]],
                    )

                    word_element.text = word
                except KeyError:
                    continue

    xml_str = ET.tostring(root, encoding="utf-8")

    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="  ")

    return pretty_xml_str


src_folder = "./lab1_2/movie_reviews"

dst_folder = "./lab1_2/movie_reviews_converted"
os.makedirs(dst_folder, exist_ok=True)

for root_dir, dirs, files in os.walk(src_folder):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root_dir, file), "r") as f:
                text = f.read()
            #  print(file)
            xml_text = text_to_xml(text, file)

            new_dir = root_dir.replace(src_folder, dst_folder)
            os.makedirs(new_dir, exist_ok=True)
            new_file = os.path.join(new_dir, file.replace(".txt", ".xml"))

            with open(new_file, "w") as f:
                f.write(xml_text)
