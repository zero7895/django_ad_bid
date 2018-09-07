# coding: utf-8
import elasticsearch
from queue import PriorityQueue

def get_answer(query_text, index='qa_text', doc_type='text', ntop=3):
    """
    search in elastichsearch data set, given index and doc_type
    ntop: number of top result regarding to score
    return top score qa_set's answer
    """
    es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
    query_body = {
        "query": {
            "match": {
                "question": query_text
            }
        }
    }
    search = es.search(index='qa_text', doc_type='text', body=query_body)
    pq = PriorityQueue()
    for i, value in enumerate(search['hits']['hits']):
        if i == ntop:
            break
        score, answer, question = value['_score'], value['_source']['answer'], value['_source']['question']
        pq.put((score, (answer, question)))

    # return top result of top score for now, for the future, may extend functionality such as comapring score and return ntop choices
    (score, (answer, question)) = pq.get()
    return answer