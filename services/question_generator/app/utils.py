import spacy
from collections import Counter
import random
import nltk
from nltk.corpus import wordnet


nltk.download('wordnet')

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str, n: int = 5):
    doc = nlp(text)

    words = [token.text for token in doc if token.pos_ in ("PROPN", "NOUN") and token.is_alpha]

    most_common = [word for word, _ in Counter(words).most_common(n)]
    return most_common

def generate_options(answer: str, text_words: list[str], n: int = 4):
    options = set([answer])

    for syn in wordnet.synsets(answer):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", " ")
            if word.lower() != answer.lower() and word.isalpha():
                options.add(word)
            
            if len(options) >= n:
                break
        if len(options) >= n:
            break

    while len(options) < n and text_words:
        options.add(random.choice(text_words))

    return random.sample(list(options), k=n)