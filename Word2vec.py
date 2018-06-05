#from ArticleSerializer import ArticleSerializer
from Models.PhygeVariables import PhyVariables
from Storage import Storage

from gensim.test.utils import common_texts
from gensim.corpora import Dictionary
from gensim.models import Word2Vec
from gensim import models
from gensim.similarities import SoftCosineSimilarity
from gensim import corpora

import json
import os

test_number = PhyVariables.currentTestKey
tmp_path = Storage(test_number).tmp_path
test_case = Storage(test_number).load_test_case()
articles_file_name = PhyVariables.articlesFileKey
w2v_path = tmp_path + PhyVariables.modelW2vKey
#if os.path.isfile(tmp_path + articles_file_name):
#    saved_articles = ArticleSerializer.deserialize(tmp_path + articles_file_name)



saved_articles = list()
path = tmp_path + articles_file_name
if not os.path.isfile(path):
    print('Error\n')

with open(path, 'r', encoding="utf8") as file:
    articles = json.load(file)
    for obj in articles:
        saved_articles.append(obj['normalized_words'])


def load_w2v_model(w2v_path):
    print('\nword2vec model loading...')
    try:
        w2v_model = models.Word2Vec.load(w2v_path)
        print('Loaded')
    except:
        print('Модель не найдена.')
        w2v_model = None
    return w2v_model

w2v_model = load_w2v_model(w2v_path)
if not w2v_model:
    w2v_model = Word2Vec(saved_articles)
    w2v_model.save(w2v_path)
    print("Модель закружена и успешно сохранена")

dictionary = corpora.Dictionary(saved_articles)
corpus = [dictionary.doc2bow(document) for document in saved_articles]

