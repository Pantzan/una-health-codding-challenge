from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from unaapp.models import User, UserReport, GlucoseMetric
from .utils import get_sample_csv_file


BULK_CREATE_URL = reverse('create-report')


def test_insert_bulk_transfers_sample_1_ok(db, user, client):
    user.name = "aaa"
    user.save()

    filename = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED
    assert GlucoseMetric.objects.count() == 1199
    assert (
            list(
                set(GlucoseMetric.objects.all().values_list("report__id", flat=True))
            )[0] == GlucoseMetric.objects.first().report.id
    )


def test_insert_bulk_transfers_sample_2_ok(db, user, client):
    user.name = "bbb"
    user.save()

    filename = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED
    assert GlucoseMetric.objects.count() == 1369
    assert (
            list(
                set(GlucoseMetric.objects.all().values_list("report__id", flat=True))
            )[0] == GlucoseMetric.objects.first().report.id
    )


def test_insert_bulk_transfers_sample_1__fail(db, user, client):
    user.name = "aaa"
    user.save()

    filename = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert GlucoseMetric.objects.count() == 000


def test_insert_bulk_transfers_sample_2__fail(db, client):
    filename = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert GlucoseMetric.objects.count() == 000
