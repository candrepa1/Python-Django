from django.core.mail import send_mail

from cards.models import Card
from trello.celery import app


@app.task(name='notification_email')
def notification_email(members, card):
    send_mail(
        subject='You have been assigned as member of a card',
        message=f'You are now a member of card {card}',
        from_email='notifications@trello.com',
        recipient_list=members
    )


@app.task(name='deadline_email')
def deadline_email(card_id):
    card = Card.objects.get(id=card_id)
    members = card.members.all().values('email')
    for member in members:
        send_mail(
                subject='The deadline for your task is close!',
                message=f'The deadline for task {card.name} is 1 day away, please complete it as soon as possible!',
                from_email='deadlines@trello.com',
                recipient_list=[member['email']]
        )
