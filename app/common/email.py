import secrets

from flask import session, url_for
from flask_mail import Message

from app.common.celery import make_celery
from app import mail

celery = make_celery()


@celery.task
def sendmail(uid, recipient):
    session['token' + str(uid)] = secrets.token_hex(8)
    msg = Message('Email verification request',
                  sender='donotreplytesting121@gmail.com',
                  recipients=[recipient])
    msg.body = url_for("users.confirm_email", token=session['token' + str(uid)], _external=True)
    mail.send(msg)
    return 'verification email has been sent'
