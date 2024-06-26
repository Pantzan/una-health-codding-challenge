from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime


class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)


class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    timestamp = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.user} - {self.timestamp}'


class GlucoseMetric(models.Model):
    RECORDING_TYPES = {
        "0": "Type 0",
        "1": "Type 1",
        "2": "Type 2",
        "3": "Type 3",
        "4": "Type 4",
        "5": "Type 5",
        "6": "Type 6",
    }
    report = models.ForeignKey(UserReport, on_delete=models.CASCADE, related_name='metrics', null=True)
    device = models.CharField(max_length=30, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    device_timestamp = models.DateTimeField()
    recording_type = models.PositiveIntegerField(choices=RECORDING_TYPES)
    glucose_value_ml = models.IntegerField(null=True, blank=True, db_index=True)
    glucose_scan_ml = models.IntegerField(null=True, blank=True)

    # other fields emitted for simplicity

    def __str__(self):
        return f'{self.serial_number} - {self.device_timestamp}'


@receiver(pre_save, sender=GlucoseMetric)
def validate_ml_values(sender, instance, **kwargs):
    if instance.glucose_value_ml not in range(-1, 200):
        raise ValidationError("glucose_value_ml should be range -1 and 200")

    if instance.glucose_scan_ml not in range(-1, 200):
        raise ValidationError("glucose_value_ml should be range -1 and 200")

    if instance.id is None:
        instance.device_timestamp = timezone.make_aware(str(instance.device_timestamp), timezone.get_current_timezone())
