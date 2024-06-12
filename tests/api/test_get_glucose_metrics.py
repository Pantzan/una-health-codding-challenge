from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from .utils import get_sample_csv_file

GET_METRICS_URL = reverse('get-glucose-levels-by-user')
BULK_CREATE_URL = reverse('create-report')


def test_get_all_metrics_for_user_a(db, user, client):
    user.name = "aaa"
    user.save()

    filename = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(GET_METRICS_URL, data={'user': "aaa", "limit": 10})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("results")) == 10


def test_get_all_metrics_for_user_a_with_start(db, user, client):
    user.name = "aaa"
    user.save()

    filename = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(GET_METRICS_URL, data={'user': "aaa", "limit": 10, 'start': 20})
    data = response.json().get("results")

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 10
    assert data[0].get("glucose_value_ml") > 20
    assert data[-1].get("glucose_value_ml") > 20


def test_get_all_metrics_for_user_a_empty(db, user, client):
    user.name = "aaa"
    user.save()

    filename = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv'
    csv_file_contents = get_sample_csv_file(filename)
    upload_file = SimpleUploadedFile(filename, csv_file_contents, content_type='multipart/form-data')
    response = client.post(BULK_CREATE_URL, data={'report_file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(GET_METRICS_URL, data={'user': "bbb", "limit": 10, 'start': 20})
    data = response.json().get("results")

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 0


def test_get_single_glucose_metric(db, user, glucose_metric, client):
    user.name = "aaa"
    user.save()

    response = client.get(reverse('get-glucose-levels-by-id', args=[glucose_metric.id]))
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, dict)
    assert data.get('id') == glucose_metric.id


def test_get_single_glucose_metric__empty(db, user, glucose_metric, client):
    user.name = "aaa"
    user.save()

    response = client.get(reverse('get-glucose-levels-by-id', args=[4]))
    assert response.status_code == status.HTTP_404_NOT_FOUND
