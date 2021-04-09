import pytest
from io import BytesIO
from faker import Faker
from PIL import Image

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from main_app.models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User


# faker = Faker()
#
# import mock
# from django.core.files import File
#
# file_mock = mock.MagicMock(spec=File, name='FileMock')
#
# image_file = BytesIO()
# image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
# image.save(image_file, 'png')
# image_file.name = 'test.png'
# image_file.seek(0)
# django_friendly_file = ContentFile(image_file.read(), 'test.png')


@pytest.mark.django_db
def test_home_page_view(client):
    url = reverse('home_page')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_authorization_page_view(client):
    url = reverse('authorization')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_organs_list_view(client):
    url = reverse('organs_list')
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_organ_create_view(client):
#     url = reverse('add_organ')
#     data = {
#         'name': 'test organ',
#         'description': 'test description',
#         'image': SimpleUploadedFile('test.jpg', b'test')
#     }
#     response = client.post(url, data)
#     organ = Organ.objects.get(name='test organ')
#     assert response.status_code == 302
#     assert Organ.objects.count() == 1
#     assert organ


@pytest.mark.django_db
def test_geographical_area_list_view(client):
    url = reverse('geographical_areas_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_treatments_list_view(client):
    url = reverse('treatments_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_treatment_create_view(client):
    url = reverse('treatments_list')
    response = client.post(url, {'treatment': 'test treatment'})
    treatment = Treatment.objects.get(treatment='test treatment')
    assert response.status_code == 302
    assert treatment


@pytest.mark.django_db
def test_symptoms_list_view(client):
    url = reverse('symptoms_list')
    response = client.get(url)
    assert response.status_code == 200

