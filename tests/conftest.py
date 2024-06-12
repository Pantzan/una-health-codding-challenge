from datetime import datetime
from pathlib import Path

import pytest
from rest_framework.test import APIClient
from django.core.management import call_command

from unaapp.models import User, UserReport, GlucoseMetric


@pytest.fixture()
def user(db):
    return User.objects.create(
        name="test_user"
    )


@pytest.fixture()
def user_report(db, user):
    return UserReport.objects.create(
        user=user,
        timestamp=datetime.now()
    )


@pytest.fixture()
def glucose_metric(db, user_report):
    return GlucoseMetric.objects.create(
        report=user_report,
        device="FreeStyle LibreLink",
        serial_number="1D48A10E-DDFB-4888-8158-026F08814832",
        device_timestamp="2021-02-14T16:50:00Z",
        recording_type=0,
        glucose_value_ml=121,
        glucose_scan_ml=30
    )


@pytest.fixture
def client():
    return APIClient()


