import logging
from django.core.mail import EmailMessage

from datapoints.models import Alert

def check_alert(circuit, measurement):
    try:
        alerts = Alert.objects.filter(circuit=circuit)

        for alert in alerts:
            print(alert)
            if(not alert.min_val <= measurement.magnitude <= alert.max_val):
                email(alert, measurement)
    except:
        logger = logging.getLogger(__name__)
        logger.warn("Couldn't send alert for " + str(circuit))


def email(alert, measurement):
    msg = """Hello {name}"""
    recipient = alert.email
    email = EmailMessage(body=msg, subject="thing", to=[recipient])
    email.send(fail_silently=False)
