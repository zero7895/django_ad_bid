from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from adgeek.nateFolder import bid

@csrf_exempt
def adgeek_nate(request):
    print(settings.BASE_DIR)
    if request.method == "POST":	
        ad_id = request.POST.get('adgeek_ad')
        is_get_ad = request.POST.get('adgeek_ad_result')
        print('ad_id:', ad_id)
        print('is_get_ad:' , is_get_ad)        
        if ad_id and is_get_ad == None:
            print( "[adgeek_ad] id:", ad_id )
            #bid the ad for the price
            price = bid.handleRequest(ad_id)
            print('price', price)
            return  JsonResponse({'ad_id': ad_id, 'price': price})

        if ad_id and is_get_ad:
            print( "[adgeek_ad] id:", ad_id )
            print( "[adgeek_ad] success::", is_get_ad )
            bid.updateRecord(ad_id)
            return  JsonResponse({ ad_id: 'ok'})

        return JsonResponse({})

