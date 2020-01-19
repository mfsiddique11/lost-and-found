from flask_mail import Message

from app.common.celery import make_celery
from app import mail

celery = make_celery()


@celery.task()
def sendmail(token, recipient):
    msg = Message('Email verification request',
                  sender='donotreplytesting121@gmail.com',
                  recipients=[recipient])
    msg.body = token
    mail.send(msg)
