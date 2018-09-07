# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from lib.search import get_answer
from lib import search
from lib import train

@csrf_exempt
def adgeek_api(request):
    if request.method == "POST":
        post_val = request.POST.get('adgeek_message')
        print("[adgeek_api] post request:", request)
        print("[adgeek_api] adgeek_message is :", post_val)
        response = search.get_answer(post_val)
        print(response)
        responseStr = '[POST] return json for adgeek_message is:' + response
        return  JsonResponse({'adgeek_response': responseStr})

    elif request.method == "Get":
        print("[adgeek_api] get request:", request)
        return  JsonResponse({'adgeek_api':'get test'})
    
@csrf_exempt
def adgeek_post_qa(request):
    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        index = request.POST.get('index')
        doc_type = request.POST.get('doc_type')
        idx = request.POST.get('id')
        if idx is None:
            idx = '1'
#         print(question, answer, index, doc_type, idx)
        resp = train.upload_qa(question, answer, index=index, doc_type=doc_type, idx=idx)
        responseStr = question + answer + str(index) + str(doc_type) + str(idx) + resp
        return  JsonResponse({'adgeek_response': responseStr})

# def test(text):
#     response = get_answer(text)
#     print(response)
    
# if __name__ == '__main__':
#     test('颱風')
