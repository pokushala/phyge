from Interface import Interface
import json
import settings

if __name__ == '__main__':
    interface = Interface()
    interface.start_engine()
    #interface.get_result()
    m1, m2, m3 = interface.get_result()
    i=0
    for m in m1:
        print('%s answer time for %s'% (m["answer_time"], m["model_name"]))
        with open('answer'+m["model_name"]+str(i)+".json", 'w', encoding="utf8") as file:
            i+=1
            s = json.dumps(m["answer_articles"], indent=2, ensure_ascii=False)
            file.write(s)
    for m in m2:
        print('%s answer time for %s'% (m["answer_time"], m["model_name"]))
        with open('answer'+m["model_name"]+str(i)+".json", 'w', encoding="utf8") as file:
            i+=1
            s = json.dumps(m["answer_articles"], indent=2, ensure_ascii=False)
            file.write(s)
    for m in m3:
        print('%s answer time for %s'% (m["answer_time"], m["model_name"]))
        with open('answer'+m["model_name"]+str(i)+".json", 'w', encoding="utf8") as file:
            i+=1
            s = json.dumps(m["answer_articles"], indent=2, ensure_ascii=False)
            file.write(s)
