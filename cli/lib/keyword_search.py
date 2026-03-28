import string

from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        preprocessed_query = preprocesse_text(query)
        preprocessed_title = preprocesse_text(movie["title"])
        if preprocessed_query in preprocessed_title:
            results.append(movie)
            if len(results) >= limit:
                break
    return results


def preprocesse_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def tokenize(input: str) -> list:
    puncDic = {}
    for punc in string.punctuation:
        puncDic[punc] = None
    puncTrans = str.maketrans(puncDic)
    output = input.lower().translate(puncTrans)
    print(output)
    return ""