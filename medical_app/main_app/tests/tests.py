import pytest

from django.urls import reverse

from main_app.models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User


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

