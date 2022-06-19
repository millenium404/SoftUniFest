from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Discount, POS


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
    import requests
    app_clients = User.objects.filter(is_client=True)
    app_clients_emails = [client.email for client in app_clients]
    # Read Clients from bank API
    endpoint = 'http://localhost:8000/clients/'
    get_response = requests.get(endpoint)
    api_clients = get_response.json()
    for api_client in api_clients:
        if api_client['email'] not in app_clients_emails:
            User.objects.create(
                username=api_client['username'],
                password=api_client['password'],
                name=api_client['name'],
                email=api_client['email'],
                phone=api_client['phone'],
                card_number=api_client['card_number'],
                card_expires=api_client['card_expires'],
                is_client=True
            )
    # Read Merchants from bank API
    endpoint = 'http://localhost:8000/merchants/'
    get_response = requests.get(endpoint)
    api_merchants = get_response.json()
    app_merchants = User.objects.filter(is_merchant=True)
    app_merchants_emails = [
        merchant.email for merchant in app_merchants]
    for api_merchant in api_merchants:
        if api_merchant['email'] not in app_merchants_emails:
            User.objects.create(
                username=api_merchant['username'],
                password=api_merchant['password'],
                name=api_merchant['name'],
                email=api_merchant['email'],
                phone=api_merchant['phone'],
                is_merchant=True
            )
    # Read BankStaff from bank API
    endpoint = 'http://localhost:8000/staff/'
    get_response = requests.get(endpoint)
    api_bankstaff = get_response.json()
    app_staff = User.objects.filter(is_staff=True)
    app_staff_emails = [
        staff.email for staff in app_staff]
    for api_staff in api_bankstaff:
        if api_staff['email'] not in app_staff_emails:
            User.objects.create(
                username=api_staff['username'],
                password=api_staff['password'],
                name=api_staff['name'],
                email=api_staff['email'],
                is_staff=True
            )
    # Read POS from bank API
    endpoint = 'http://localhost:8000/pos/'
    get_response = requests.get(endpoint)
    api_pos_terminals = get_response.json()
    app_pos = POS.objects.all()
    app_pos_serial_nums = [
        pos.serial_number for pos in app_pos]
    for api_pos in api_pos_terminals:
        if api_pos['serial_number'] not in app_pos_serial_nums:
            POS.objects.create(
                user=api_pos['merchant'],
                serial_number=api_pos['serial_number'],
            )
