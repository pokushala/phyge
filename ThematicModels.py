import time
from gensim import corpora, models, similarities

from Storage import Storage


class BaseModel:
    """BaseModel class realise methods repeated for all models like forming corpus and queries,
       finding articles and performing results.
       LSImodel, LDAmodel, W2Vmodel classes inherites from BaseModel where defines their own fields base_model
        and train methods
    """
    TOPIC_NUMBER = 300

    def __init__(self, storage: Storage, model_name='model'):
        self.storage = storage
        self.dct = storage.get_dct()
        self.corpus = storage.get_corpus().copy()
        #self.dct.save(self.storage.tmp_path + '/deerwester.dict')
        #corpora.MmCorpus.serialize(self.storage.tmp_path + '/deerwester.mm', self.corpus)
        self.base_model = storage.get_model(model_name)
        self.model_name = model_name
        self.train_models()

    def train_models(self):
        if self.base_model is None:
            self.base_model = self.train_model()
            self.save_model()

    def save_model(self):
        self.storage.save_model(self.base_model, self.model_name)


    # ЭТО ДОЛЖНО БЫТЬ В ИНТЕРФЕЙСЕ
    def find_article(self, query_text, amount=5):
        return self.perform_search(self.base_model[self.corpus], self.base_model[query_text], amount)

    def perform_search(self, corpus_model, query_vec, amount):
        start_time = time.time()
        index = similarities.MatrixSimilarity(corpus_model)
        sims = index[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        answer_time = round((time.time() - start_time), 3)
        articles = self.storage.get_articles()
        found_articles = []
        for i, similarity in sims[:amount]:
            article_similarity = articles[i].copy()
            article_similarity.update({'id': i,
                                       'similarity': round(float(similarity), 3)})
            article_similarity['text'] = (articles[i]['text'][:200]).replace("', '", '').replace("['", '') + '...'
            article_similarity.pop('normalized_words')
            found_articles.append(article_similarity)
        return answer_time, self.model_name, found_articles



    # вот это вот должно передавать результат в тело а тело в интерфейс
    def show_result_info(self, amount=3):
        answers = []
        for query in self.storage.get_queries():
            query_text = query['text']
            query_vec = self.storage.query_to_vec(query_text)
            answer_time, model_name, answer_articles = self.find_article(query_vec, amount=amount)
            answers.append({'answer_time':answer_time,
                            'model_name': model_name,
                            'answer_articles':answer_articles})
        return answers



class LSImodel(BaseModel):
    def __init__(self, storage: Storage):
        #super().__init__(self, storage)
        BaseModel.__init__(self, storage=storage, model_name='lsi')

    def train_model(self):
        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        lsi = models.LsiModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lsi


class LDAmodel(BaseModel):
    def __init__(self, storage: Storage):
        #super().__init__(storage)
        BaseModel.__init__(self, storage=storage, model_name='lda')

    def train_model(self):
        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        lda = models.ldamodel.LdaModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER,
                                       passes=20)  # ,iterations=50)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lda


class W2Vmodel(BaseModel):
    def __init__(self, storage: Storage):
        #super().__init__(storage)
        BaseModel.__init__(self, storage=storage, model_name='w2v')

    def find_article(self, query_text, amount=5):
        return super().perform_search(self.corpus, query_text, amount)

    def train_model(self):
        print('\nWord2vec model: Обучаем модель...')
        start_time = time.time()
        #documents = []
        documents = self.storage.get_words_list()
        w2v = models.Word2Vec(documents, min_count=5)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return w2v
