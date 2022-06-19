from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Discount


def send_mail_to_clients():
    users = User.objects.all()
    discounts = Discount.objects.all().filter_by(status='active')
    message_content = 'Здравейте, това са новите отстъпки: \n'
    for item in discounts:
        message_content += f"{item.user.porfile.name}: {stritem.percent} до дата {item.end_date}"
    for user in users:
        if user.profile.is_client:
            send_mail(
                        'Нови отстъпки',
                        message_content,
                        'pos@postbank.bg',
                        [user.email],
                        fail_silently=False,
                    )


def send_mail_to_merchants(user_id, discount_id):
    user = Users.objects.get(id=user_id)
    discount = Discount.objects.get(id=discount_id)
    if discount.status == 'active':
        message_content = f'''Здравейте, имате активирана отстъпка:
{discount.id} за периода от {discount.start_date}, {discount.end_date}'''
        send_mail(
                    'Активна отстъпка',
                    message_content,
                    'pos@postbank.bg',
                    [user.email],
                    fail_silently=False,
                )
def sync_databases():
    pass
