import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
about_interest_text = ('He is interested in learning Natural Language Processing.')
about_interest_doc = nlp(about_interest_text)
displacy.render(about_interest_doc, style='dep')