from django.db import models

from django.core.validators import MinValueValidator, MaxLengthValidator


class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)


class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    timestamp = models.DateTimeField(null=False)


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
    glucose_value_ml = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(limit_value=-1),
            MaxLengthValidator(limit_value=300)
        ]
    )
    glucose_scan_ml = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(limit_value=-1),
            MaxLengthValidator(limit_value=300)
        ]
    )
    # other fields emitted for simplicity

    def __str__(self):
        return f'{self.serial_number} - {self.device_timestamp}'
