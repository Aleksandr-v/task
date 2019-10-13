from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


MESSAGE = """
От {}

{}

Город {}
улица {}
квартира {}
почтовый индекс {}

Email {}
Номер телефона {}
"""


def send_feedback(body, email, sender):
    subject = 'Test Task'
    email_from = settings.EMAIL_HOST_USER
    admin = get_user_model().objects.filter(is_superuser=True) \
                            .order_by('-id')[0]
    recipient_list = [admin.email]
    message = ''
    if not sender:
        message = body + '\n\rEmail ' + email
    else:
        message = MESSAGE.format(
            sender['name'], body, sender['address']['city'],
            sender['address']['street'], sender['address']['suite'],
            sender['address']['zipcode'], email, sender['phone']
        )
    print(message)
    return send_mail(subject, message, email_from, recipient_list)
