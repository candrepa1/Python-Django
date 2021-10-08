from django.core.mail import send_mail

from trello.celery import app


@app.task(name='invitation_email')
def invitation_email(data, message):
    send_mail(
        subject='new board invitation',
        html_message=f'<html><body><h1>{data["name"]}, you have been invited to board {data["board"]}!</h1>{message}</body></html>',
        message='',
        from_email='invitations@trello.com',
        recipient_list=[data['email']]
    )
