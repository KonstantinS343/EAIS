from nltk.text import Text
from nltk.corpus import movie_reviews


def find_context(word: str, length: int, count: int) -> str:
    text = Text(movie_reviews.words())
    con_list = text.concordance_list(word, width=length, lines=count)
    return "\n".join([str(i + 1) + ". " + j.line for i, j in enumerate(con_list)])
