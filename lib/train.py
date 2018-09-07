# coding: utf-8
import elasticsearch
import pandas as pd

# import jieba
# import jieba.analyse


# constant parameters
DATA_PATH = '../data/'
QA_SET_RAW = DATA_PATH + 'qa_set_raw.csv'
QA_SET_CUT = DATA_PATH + 'qa_set_cut.csv'
DICT_PATH = 'jieba_dict/dict.txt.big'
STOP_WORDS_DIC = 'jieba_dict/stopwords.txt'
WORDVEC_MODEL_PATH = 'word2vec_model/word2vec.model'
SCORE_THRESHOLD = 0.1

# global variable
stopword_set = set()

def load_jieba_dict():
    """
    loading jieba custom dictionary and stopwords
    """
    print('load_jieba_dict():')
    jieba.set_dictionary(DICT_PATH)
    with open(STOP_WORDS_DIC, 'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))
            
def cut_raw_set(path):
    load_jieba_dict()
    df = pd.read_csv(QA_SET_RAW, sep=',', header=0, encoding='utf-8')
    questions, answers = [], []
    for index, row in df.iterrows():
        q_text = ' '.join(jieba.cut(row['question']))
        q_filtered = list(filter(lambda x: x not in stopword_set, q_text))
        questions.append(q_filtered)
        
        a_text = ' '.join(jieba.cut(row['answer']))
        a_filtered = list(filter(lambda x: x not in stopword_set, a_text))
        answers.append(a_filtered)
    df = pd.DataFrame({'question' : questions, 'answer' : answers})
    df.to_csv(DATA_PATH + 'qa_set_cut.csv', encoding='utf-8')
    
def create_qa_body(question, answer):
    body = {
        "question": question,
        "answer": answer
    }
    return body

def upload_qa_csv(path, es, index='qa_text', doc_type='text'):
    """
    path: path of input data set
    es: instance of elasticsearch
    """
    df = pd.read_csv(path, encoding='utf-8')
    for id, row in df.iterrows():
        question, answer = row['question'], row['answer']
        body = create_qa_body(question, answer)
        es.create(index=index, doc_type=doc_type, id=str(id), body=body, ignore=[409])
        
def upload_qa(question, answer, index='other', doc_type='text', idx=None):
    es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if index is None:
        index = 'other'
    if doc_type is None:
        doc_type = 'text'
    body = create_qa_body(question, answer)
    print(question, answer, index, doc_type, idx)
    if idx:
        resp = es.create(index=index, doc_type=doc_type, idx=idx, body=body, ignore=[409])
    else:
        try:
            resp = es.create(index=index, doc_type=doc_type, body=body, ignore=[409])
        except:
            return "  create error"
    return str(resp)


if __name__ == '__main__':
    es = elasticsearch.Elasticsearch()
#     put_qa_set(QA_SET_RAW, es)
    
    