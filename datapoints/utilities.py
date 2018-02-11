from django.core.exceptions import ObjectDoesNotExist

from datapoints.models import Device


def get_or_add_device(mac):
    try:
        device = Device.objects.get(mac=mac)
        return device
    except ObjectDoesNotExist:
        new_device = Device()
        new_device.mac = mac
        new_device.save()
        new_device.name = "New Device " + str(new_device.id)
        new_device.save()
        return new_device
