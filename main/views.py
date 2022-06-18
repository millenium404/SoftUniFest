import datetime
from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Discount, POS
from accounts.models import Profile


def convert_date(string):
    string = string.split('/')
    string = [int(num.lstrip('0')) for num in string]
    year = string[2] + 2000
    date_object = datetime.date(string[2], string[1], string[0])
    return date_object


@login_required
def merchant_view(request, id):
    context = {}
    if id == request.user.id:
        if request.POST:
            query = request.POST.dict()
            if 'notifications' in query:
                profile = Profile.objects.get(user=request.user)
                if request.POST['notifications'] == 'Изпращай известия':
                    profile.notifications = True
                else:
                    profile.notifications = False
                profile.save()
            else:
                try:
                    discount = Discount(
                        user=request.user,
                        percent=query['discount'],
                        start_date = convert_date(query['start']),
                        end_date = convert_date(query['end'])
                    )
                    discount.save()
                except:
                    pass
        discounts = Discount.objects.filter(user=request.user)
        context['discounts'] = discounts
        return render(request, 'home-merchant.html', context)
    else:
        raise Http404


@login_required
def staff_view(request):
    discounts = Discount.objects.all()
    for discount in discounts:
        try:
            if len(discount.staff_decisions.split(',')) > 2:
                discount.status = 'active'
                discount.save()
        except:
            pass
    if request.POST:
        discount_id = int(request.POST['approved'])
        print(discount_id)
        discount = Discount.objects.get(id=discount_id)
        discount.staff_decisions += str(request.user.id) + ','
        discount.save()
        return redirect('staff-view')
    merchants = Profile.objects.filter(is_merchant=True)
    discounts = Discount.objects.all()
    terminals = POS.objects.all().order_by('user')
    user_id = str(request.user.id)
    context = {
        'merchants': merchants,
        'discounts': discounts,
        'terminals': terminals,
        'user_id': user_id
    }
    return render(request, 'home-staff.html', context)


@login_required
def client_view(request):
    if request.POST:
        profile = Profile.objects.get(user=request.user)
        if request.POST['notifications'] == 'Изпращай известия':
            profile.notifications = True
        else:
            profile.notifications = False
        profile.save()
    discounts = Discount.objects.all()
    card_number = request.user.profile.card_number
    card_number = card_number[0:4] + ' **** **** ' + card_number[-4:]
    context = {
        'discounts': discounts,
        'card_number': card_number
    }
    return render(request, 'home-client.html', context)
