import os
import smtplib

class Notify(object):
    EMAIL = os.getenv("gmail_email")
    PASSWORD = os.getenv("gmail_password")
    RECIPIENT = os.getenv("gmail_recipient")
    ENABLED = True

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL, PASSWORD)
    BODY = '\r\n'.join(['To: {to}',
                        'From: {sender}',
                        'Subject: {subject}',
                        '{text}'])

    @classmethod
    def notify(cls, timestamp):
        formatted_timestamp = timestamp.strftime("%m-%d-%y %I:%M:%S %p")
        message = cls.BODY.format(
            to=cls.RECIPIENT,
            sender=cls.EMAIL,
            subject="Movement detected at {}".format(formatted_timestamp),
            text="Movement was detected at 318 Rindge Ave. U304 Cambridge MA 02140"
        )
        cls.server.sendmail(cls.EMAIL, [cls.RECIPIENT], message)
