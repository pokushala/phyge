import Engine


class Interface:
    def __init__(self, language='ru'):
        self.query = ""
        self.language = language
        self.result = None

    # ожидает текстовый запрос
    def set_text(self, query):
        self.query = query
        self.start_engine()

    # ожидает речевой запрос
    def listen(self):
        self.start_engine()

    # спрашивает у тела готов ли результат
    def get_result(self):
        return self.result

    def start_engine(self):
        engine = Engine(self.query)
        self.result = engine.get_result()
