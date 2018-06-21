from Storage import Storage
from Parser import Parser
from ThematicModels import LDAmodel, LSImodel, W2Vmodel


# query will be taken from interface but now we take it from storage
class Engine:
    def __init__(self, query):
        self.storage = Storage()
        self.parser = Parser()

        self.query = query
        self.new_urls = None
        self.load_by_urls()
        self.lda_model = LDAmodel(self.storage)
        self.lsi_model = LSImodel(self.storage)
        self.w2v_model = W2Vmodel(self.storage)


    #def get_model(self, model): # получаем модель из Storage
    def check_if_new_urls(self):  # проверяет есть ли новые ссылки
        self.new_urls = self.storage.get_new_urls()
        if self.new_urls:
            return True
        return False

    # в articles будут только новые новые статьи
    def load_by_urls(self):  # загрузка текстов по ссылкам
        if self.check_if_new_urls():
            self.parser.load_articles(self.storage, self.new_urls)


    #def send_to_model(self): # отправляет запрос в модель
    def get_result(self):  # возвращает результат
        return self.lda_model.show_result_info(), self.lsi_model.show_result_info(), self.w2v_model.show_result_info()
