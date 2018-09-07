from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from adgeek.tony_folder import bid


@csrf_exempt
def adgeek_tony(request):
    if request.method == "POST":
        ad_id = request.POST.get('adgeek_ad')
        is_get_ad = request.POST.get('adgeek_ad_result')
        print('ad_id:', ad_id)
        print('is_get_ad:' , is_get_ad)
        if ad_id and (is_get_ad is None):
            print( "[adgeek_ad] id:", ad_id )
            #bid the ad for the price
            bidding_price = bid.bid(ad_id)
            return  JsonResponse({'ad_id': ad_id, 'price': bidding_price})
        if ad_id and (is_get_ad is not None):
            print( "[adgeek_ad] id:", ad_id )
            print( "[adgeek_ad] success::", is_get_ad )
            bid.write_record(is_get_ad=is_get_ad)
            return  JsonResponse({ ad_id: is_get_ad})

        return JsonResponse({})