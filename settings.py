
# тут лежат названия папок и номер папки с ссылками
import os

# тесты
tests_dir = 'Resourses'
test_case_id = 4
test_case_path = str.format('{0}/test_{1}', tests_dir, test_case_id)

# содержание папки с тестами json с ссылками 
# и json с  текстовыми запросами
urls_file_key = 'urls.json'
urls_path = os.path.join(test_case_path, urls_file_key)

queries_file_key = 'queries.json'
queries_path = os.path.join(test_case_path, queries_file_key)

# папка tmp в нее складываются создаваемые файлы
tmp_path = test_case_path + '/tmp/'

# urlsFileKey = 'en_slack_urls_clear.json'
articles_fle_key = 'articles.json'
articles_path = tmp_path + articles_fle_key

words_list_file_key = 'values.csv'
words_list_path = tmp_path + words_list_file_key

urls_status_file_key = 'urls.status.json'
urls_status_path = tmp_path + urls_status_file_key

# модели
model_lsi_key = 'phydge.lsi'
model_lda_key = 'phydge.lda'
model_w2v_key = 'phydge.w2v'
lsi_path = tmp_path + model_lsi_key
lda_path = tmp_path + model_lda_key
w2v_path = tmp_path + model_w2v_key

dct_key = 'deerwester.dict'
dct_path = tmp_path + dct_key


ref_dir = 'ref'
stopwords_dir = 'stopwords'
ru_stopwords_key = 'russian'
ru_en_stopwords_key = 'russian_english'
ru_stopwords_path = os.path.join(ref_dir, stopwords_dir, ru_stopwords_key)
ru_en_stopwords_path = os.path.join(ref_dir, stopwords_dir, ru_en_stopwords_key)