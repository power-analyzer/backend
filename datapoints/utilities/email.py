import logging
import code

from smtplib import SMTPException
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from datapoints.models import Alert

def check_alert(circuit, measurement):
    try:
        alerts = Alert.objects.filter(circuit=circuit)
        time = measurement.time
        for alert in alerts:
            latest_valid_time = time - timezone.timedelta(minutes=alert.frequency_limit)
            # code.interact(local=locals())
            if((latest_valid_time >= alert.last_used) and \
                    ((alert.min_val and getattr(measurement, alert.attribute) <= alert.min_val) or \
                    ( alert.max_val and getattr(measurement, alert.attribute) >= alert.max_val))):
                email(alert, measurement, circuit)
                alert.last_used = time
                alert.save()
                return True
    except SMTPException:
        logger = logging.getLogger(__name__)
        logger.warn("Couldn't send alert for " + str(circuit))
    return False


def email(alert, measurement, circuit):
    recipient = alert.email
    name = recipient.split("@")[0].split(".")[0].capitalize()
    template_vars = {
        "name": name,
        "circuit_name": str(circuit),
        "power": getattr(measurement, alert.attribute),
        "min": alert.min_val if alert.min_val else "Anything",
        "max": alert.max_val if alert.max_val else "Anything",
        "SERVER_URL": settings.SERVER_URL
    }
    msg = email_template.format(**template_vars)
    email = EmailMessage(body=msg, subject="Power Alert", to=[recipient])
    email.send(fail_silently=False)

# TODO: IDK why I didn't write this as a Django template.
email_template = '''\
Hello {name},

Circuit {circuit_name} is using {power} watts of electricity.
This is not between your allowable range of {min} to {max}.

Login to {SERVER_URL} for more information.
Thanks!
- Power Bot
'''
