import settings

import json
import os
import pandas as pd
from gensim import models
from gensim import corpora

from TextNormalizer import TextNormalizer

class Storage:
    """
    взаимодействие с файловой системой
    class realize methods for getting and saving data
    """
    def __init__(self):
        self.test_case_id = settings.test_case_id
        self.test_case_path = settings.test_case_path
        self.tmp_path = settings.tmp_path
        self.lsi_path = settings.lsi_path
        self.lda_path = settings.lda_path
        self.w2v_path = settings.w2v_path
        self.urls_path = settings.urls_path
        self.queries_path = settings.queries_path
        self.articles_path = settings.articles_path
        self.words_list_path = settings.words_list_path
        self.urls_status_path = settings.urls_status_path
        self.dct_path = settings.dct_path

        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    # достать ссылки из памяти компьютера в оперативную память
    def get_urls(self, key='language'):
        """
        get urls from json file and save to list urls
        :return: list of dictionaries with url and language or status
        """
        urls = []
        if key == 'language':
            load_path = self.urls_path
        else:
            load_path = self.urls_status_path
        if not os.path.isfile(load_path):
            return list()
        with open(load_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
            for u in data_urls:
                urls.append(dict(url=u.get('url'), info=u.get(key, '')))
        return urls

    def get_new_urls(self):
        """
        compare urls data file with urls status generated file
        (comment variant doesn't take into account urls order)
        :return: list with new urls
        """
        db_urls = [x.get('url') for x in self.get_urls(key='language')]
        old_urls = [x.get('url') for x in self.get_urls(key='status')]
        #new_urls = list(set(db_urls) - set(old_urls))
        sbuf = set(old_urls)
        new_urls = [x for x in db_urls if x not in sbuf]
        return new_urls

    # должны принимать  полный список ссылок
    def save_urls_status(self, urls_status_list):
        """
        save full list with urls status into file
        :param urls_status_list: list with urls status
        :return:
        """
        urls_status = []
        if os.path.isfile(self.urls_status_path):
            urls_status = self.get_urls('status')
        urls_status = urls_status + urls_status_list
        with open(self.urls_status_path, 'w', encoding="utf8") as file:
            s = json.dumps(urls_status, indent=2, ensure_ascii=False)
            file.write(s)

    # сохраняем статьи в файл articles
    def save_articles(self, articles_list):
        """
        save article list into file
        :param articles_list: article list
        :return:
        """
        articles = []
        if os.path.isfile(self.articles_path):
            articles = self.get_articles()
        articles = articles + articles_list
        with open(self.articles_path, 'w', encoding="utf8") as file:
            s = json.dumps(articles, indent=2, ensure_ascii=False)
            file.write(s)

    # достаем текст статей из списка словарей с ссылками
    # открываем json со списком словарей статей и заисываем в saved_articles
    def get_articles(self):
        """
        get article info from json file to list
        :return: list of dictionaries
        """
        saved_articles = list()
        with open(self.articles_path, 'r', encoding='utf8') as file:
            data_articles = json.load(file)
            for a in data_articles:
                saved_articles.append(a)
        return saved_articles

    def save_words_df(self):
        words_df = self.get_words_df()
        words_df.to_csv(self.words_list_path, index=False, encoding='utf8')

    # надо проверить корректность записывания новых записей в дата фрейм
    def get_words_df_json(self):
        """
        get lists of normalized words from json file with article info
        and save to
        :param articles_list: articles info list
        :return: words data frame
        """
        articles_list = self.get_articles()
        columns = [pd.Series(article["normalized_words"]) for article in articles_list]
        pairs = zip(range(len(articles_list)), columns)
        data = dict((key, value) for key, value in pairs)
        df_words_in_doc = pd.DataFrame(data)
        #df_words_in_doc.to_csv(self.words_list_path, index=False, encoding='utf8')
        return df_words_in_doc

    # получаем список нормализованых слов ИЗ ДАТАФРЕЙМА
    def get_words_df_from_csv(self):
        """
        get list of normalized words from csv file
        :return: list of normalized words
        """
        words_df = pd.DataFrame()
        if os.path.isfile(self.words_list_path):
            words_df = pd.read_csv(self.words_list_path, dtype='unicode')
        return words_df

    def get_words_list(self):
        df = self.get_words_df_json()
        words_list = []
        for columns in df.columns:
            words_list.append(df[columns].dropna().tolist())
        return words_list


    # где-то надо еще перевести запросы в нормальный вид

    # записывает запросы в список queries
    def get_queries(self):
        """
        get queries from json file
        :return: list od queries
        """
        queries = list()
        with open(self.queries_path, 'r', encoding='utf8') as file:
            data_queries = json.load(file)
            for q in data_queries:
                queries.append(q)
        return queries

    # загружаем модель из файла
    def get_model(self, model_name):
        """
        load model from file according to its type
        :param model_name: name of the model
        :return: model
        """
        print('%s model loadind...', model_name)
        if model_name == 'lsi':
            load_func = models.lsimodel.LsiModel.load
            load_path = self.lsi_path
        elif model_name == 'lda':
            load_func = models.ldamodel.LdaModel.load
            load_path = self.lda_path
        else:
            load_func = models.Word2Vec.load
            load_path = self.w2v_path
        try:
            model = load_func(load_path)
            print('Loaded')
        except:
            print('Модель не найдена.')
            model = None
        return model

    def save_model(self, model, model_name):
        """
        save trained model into file
        :param model: model
        :param model_name: model name
        :return:
        """
        if model_name == 'lsi':
            save_path = self.lsi_path
        elif model_name == 'lda':
            save_path = self.lda_path
        else:
            save_path = self.w2v_path
        model.save(save_path)
        print('Model %s saved ', model_name)

    def query_dict_to_text(self, query_dict):
        return query_dict['text']

    # сохраняет словарь для модели
    def save_dct(self):
        documents = self.get_words_list()
        dct = corpora.Dictionary(documents)
        dct.save(self.dct_path)
        return dct

    # загружает словарь для модели
    def get_dct(self):
        if os.path.isfile(self.dct_path):
            dct = corpora.Dictionary.load(self.dct_path)
        else:
            dct = self.save_dct()
        return dct

    # ГДЕ ЭТО ДОЛЖНО БЫТЬ?
    # нормализуем запрос
    def query_to_vec(self, query_text):
        query_normalize = TextNormalizer.normalize(query_text)
        dct = self.get_dct()
        return dct.doc2bow(query_normalize)

    # загружаем корпус
    def get_corpus(self):
        dct = self.get_dct()
        documents = self.get_words_list()
        return [dct.doc2bow(doc) for doc in documents]

    # сохраняем корпус
    #def save_corpus(self):
    #    corpora.MmCorpus.serialize(self.storage.tmp_path + '/deerwester.mm', self.corpus)
