import spacy
from collections import Counter
import random
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet")
nltk.download("omw-1.4")

nlp = spacy.load("en_core_web_sm")


def extract_keywords(text: str, n: int = 5) -> list[str]:
    doc = nlp(text)
    words = [token.text for token in doc if token.pos_ in ("PROPN", "NOUN") and token.is_alpha]

    most_common = [word for word, _ in Counter(words).most_common(n)]
    return most_common


def generate_options(answer: str, text_words: list[str], n: int = 4) -> list[str]:
    options = set([answer])

    for syn in wordnet.synsets(answer):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", " ")
            if (
                word.lower() != answer.lower()
                and word.isalpha()
                and len(word) > 2
            ):
                options.add(word)
            if len(options) >= n:
                break
        if len(options) >= n:
            break

    if len(options) < n:
        doc_answer = nlp(answer)
        candidates = []
        for w in set(text_words):
            if w.lower() == answer.lower() or not w.isalpha():
                continue
            sim = nlp(w).similarity(doc_answer)
            candidates.append((w, sim))

        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        for w, _ in candidates[: n * 2]: 
            if len(options) >= n:
                break
            options.add(w)

    while len(options) < n and text_words:
        w = random.choice(text_words)
        if w.lower() != answer.lower() and w.isalpha():
            options.add(w)

    return random.sample(list(options), k=n)
