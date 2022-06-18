import datetime
from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Discount, POS

'''
'discount': ['8'], 'start': ['01/01/01'], 'end': ['01/01/01']
'''
def convert_date(string):
    string = string.split('/')
    string = [int(num.lstrip('0')) for num in string]
    year = string[2] + 2000
    d = datetime.date(string[2], string[1], string[0])
    return d


@login_required
def merchant_view(request, id):
    context = {}
    if id == request.user.id:
        if request.POST:
            query = request.POST.dict()
            discount = Discount(
                user=request.user,
                percent=query['discount'],
                start_date = convert_date(query['start']),
                end_date = convert_date(query['end'])
            )
            discount.save()
        discounts = Discount.objects.filter(user=request.user)
        context['discounts'] = discounts
        return render(request, 'home-merchant.html', context)
    else:
        raise Http404
