from Interface import Interface
import json


def write_result(model_result):
    query_num = 1
    for m in model_result:
        print('%s answer time for %s' % (m["answer_time"], m["model_name"]))
        with open('answ/answer'+m["model_name"]+str(query_num)+".json", 'w', encoding="utf8") as file:
            query_num += 1
            s = json.dumps(m["answer_articles"], indent=2, ensure_ascii=False)
            file.write(s)


if __name__ == '__main__':
    interface = Interface()
    interface.start_engine()
    for model_result in interface.get_result():
        write_result(model_result)
