import requests
import os


class Mailgun:
    MAILGUN_API_URL = os.getenv('MAILGUN_API_URL')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    FROM_NAME = 'benedict'
    FROM_EMAIL = "benedictmwendwa47@gmail.com"

    @classmethod
    def send_email(cls, to_emails, subject, content):
        requests.post(
            cls.MAILGUN_API_URL,
            auth=("api", cls.MAILGUN_API_KEY),
            data={"from": f"{cls.FROM_NAME} <{cls.FROM_EMAIL}>",
                  "to": to_emails,
                  "subject": subject,
                  "text": content
                  })
        return "mail send successfully"
