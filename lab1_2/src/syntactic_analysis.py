from nltk import pos_tag, word_tokenize, RegexpParser
from nltk.tokenize import sent_tokenize
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

import string
from typing import Optional, List

#  from conf.metadata import metadata


def filter_syntactic_rows(
    data: List[str],
    search_type: Optional[str] = None,
):
    return filter(lambda x: search_type is not None and search_type in x, data)


def split_sentence(text: str) -> List[str]:
    sentences = sent_tokenize(text)
    return sentences


def main_analysis(text: str):
    #  grammer = RegexpParser(
    #      """
    #      P:   {<IN>}
    #      N:   {<NN.*>}
    #      DET: {<DT>}
    #      NP:  {<DET><N><PP>?}
    #           {<NNP>}
    #      V:   {<VB.*>}
    #      PP:  {<P><NP>}
    #      VP:  {<V><NP>}
    #           {<V><NP><PP>}
    #      S:   {<NP><VP>}
    #      """
    #  )

    grammer = RegexpParser(
        """
        NP: {<DT>?<JJ>*<NN.*>}
        P: {<IN>}
        V: {<V.*>}
        PP: {<P> <NP>}
        VP: {<V> <NP|PP>*}
        """
    )

    tagged = pos_tag(
        [word for word in word_tokenize(text) if word not in string.punctuation]
    )
    #  for i in range(len(tagged)):
    #      tagged[i] = (tagged[i][0], metadata[tagged[i][1]])
    window = CanvasFrame(width=1500, height=500)
    output = grammer.parse(tagged)
    tree = TreeWidget(window.canvas(), output)
    window.add_widget(tree, 10, 10)
    window.mainloop()

#  """
#  NP: {<DT>?<JJ>*<NN>}
#  P: {<IN>}
#  V: {<V.*>}
#  PP: {<P> <NP>}
#  VP: {<V> <NP|PP>*}
#  """

#  """
#  Группа существительных: {<артикль>?<прилагательное.*>*<существительное.*>|<имя.*>}
#  Предлог: {<предлог/подчинительный союз>}
#  Глагол: {<глагол.*>}
#  Предлог и существительное: {<Предлог> <Группа существительных>}
#  Глагольная группа: {<Глагол> <Группа существительных|Предлог и существительное>*}
#  """