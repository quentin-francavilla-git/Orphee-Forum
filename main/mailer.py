import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_grid_mailer(to, content):
    message = Mail(
        from_email='lilian.raillon@epitech.eu',
        to_emails=to,
        subject='Notification Forum Orphee',
        html_content=content)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))