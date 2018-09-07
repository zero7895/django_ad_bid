"""
budget = 10000
bidding_price
ad_id
"""

TOTAL_BUDGET = 10000.0
START_BIDDING_PRICE = 1.0
CHANGE_RATE = 1.1
RECORD_PATH = 'adgeek/tony_folder/record.txt'

def str_to_bool(s):
    if s is not bool():
        return s == 'True'
    return s

def bid(ad_id):
    if ad_id == '1':
        (budget, bidding_price, is_get_ad, exp_rate) = TOTAL_BUDGET, START_BIDDING_PRICE, False, 0
    else:
        (budget, bidding_price, is_get_ad, exp_rate) = open(RECORD_PATH, 'r').readlines()[0].split(' ')
        budget, bidding_price, is_get_ad, exp_rate = float(budget), float(bidding_price), str_to_bool(is_get_ad), int(exp_rate)
    if budget <= 0:
        return 0.0
    bidding_price *= (CHANGE_RATE ** exp_rate)
    open(RECORD_PATH, 'w').write('{0} {1} {2} {3}'.format(budget, bidding_price, is_get_ad, exp_rate))
    return bidding_price

def write_record(is_get_ad=False):
    is_get_ad = str_to_bool(is_get_ad)
    (budget, bidding_price_old, is_get_ad_old, exp_rate) = open(RECORD_PATH, 'r').readlines()[0].split(' ')
    budget, bidding_price, is_get_ad_old, exp_rate = float(budget), float(bidding_price_old), str_to_bool(is_get_ad_old), int(exp_rate)
    if is_get_ad and exp_rate > 0:
        exp_rate = 0
    else:
        if is_get_ad:
            budget -= bidding_price
            exp_rate -= 1
        else:
            exp_rate += 1
    open(RECORD_PATH, 'w').write('{0} {1} {2} {3}'.format(budget, bidding_price, is_get_ad, exp_rate))