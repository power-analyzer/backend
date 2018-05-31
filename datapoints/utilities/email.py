import logging
from django.core.mail import send_mail

from datapoints.models import Alert

def check_alert(circuit, measurement):
    try:
        alerts = Alert.objects.filter(circuit=circuit)

        for alert in alerts:
            print(alert)
            if(not alert.min_val <= measurement.magnitude <= alert.max_val):
                email(
                    alert.email,
                    "Circuit %s is using %s!" % (circuit, measurement.magnitude)
                )
    except:
        logger = logging.getLogger(__name__)
        logger.warn("Couldn't send alert for " + str(circuit))


def email(msg, recipient):
    send_mail(
        'Power Notification',
        msg,
        'power-analyzer@github.io',
        [recipient],
        fail_silently=False,
    )
