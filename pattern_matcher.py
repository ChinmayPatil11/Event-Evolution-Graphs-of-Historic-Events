import spacy
from spacy.matcher import Matcher
import pandas as pd
nlp = spacy.load('en_core_web_sm')


def pattern_matcher(df):
    pmatcher = Matcher(nlp.vocab)
    docs = df['Events'].apply(lambda x: nlp(x))
    trial1 = [{'DEP': 'compound', 'OP': '*'}, {'DEP': 'nsubj'}]  # main subject
    trial2 = [{'POS': 'VERB'}]  # main verb
    trial3 = [{'DEP': 'compound', 'OP': '*'}, {'DEP': {'IN': ['nobj', 'pobj', 'dobj']}}]  # main object
    pmatcher.add('Noun', [trial1])
    pmatcher.add('Verb', [trial2])
    pmatcher.add('Objects',  [trial3])
    nounlist, verblist, objectlist = [], [], []
    for doc in docs:
        matches = pmatcher(doc)
        inner_noun, inner_verb, inner_object = [], [], []
        for match_id, start, end in matches:
            if match_id == 1882071534088494249:
                if doc[start:end] not in inner_noun:
                    inner_noun.append(doc[start:end])
            elif match_id == 14677086776663181681:
                if doc[start:end] not in inner_verb:
                    inner_verb.append(doc[start:end])
            else:
                if doc[start:end] not in inner_object:
                    inner_object.append(doc[start:end])
        nounlist.append(inner_noun)
        verblist.append(inner_verb)
        objectlist.append(inner_object)
    years = df['Year'].tolist()
    entity_relation_df = pd.DataFrame({'subject': nounlist, 'verb': verblist, 'object': objectlist, 'year':years})
    return entity_relation_df