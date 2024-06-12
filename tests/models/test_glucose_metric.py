import pytest
from django.core.exceptions import ValidationError


def test_glucose_metric_create_ok(glucose_metric):
    assert glucose_metric.id is not None
    assert glucose_metric.glucose_value_ml > 0
    assert glucose_metric.glucose_scan_ml > 0


def test_glucose_metric_create__value_fail(glucose_metric):
    with pytest.raises(ValidationError):
        glucose_metric.glucose_value_ml = -12
        glucose_metric.save()

    with pytest.raises(ValidationError):
        glucose_metric.glucose_scan_ml = -12
        glucose_metric.save()
