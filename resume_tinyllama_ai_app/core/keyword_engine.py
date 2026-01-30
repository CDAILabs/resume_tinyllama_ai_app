import spacy
from keybert import KeyBERT

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_keywords(text):
    doc = nlp(text.lower())
    nouns = {
        t.text for t in doc
        if t.pos_ in ("NOUN", "PROPN") and not t.is_stop
    }

    keybert_kw = kw_model.extract_keywords(
        text, top_n=20, stop_words="english"
    )

    return nouns.union({k for k, _ in keybert_kw})

def missing_keywords(resume_text, jd_text):
    return sorted(extract_keywords(jd_text) - extract_keywords(resume_text))
