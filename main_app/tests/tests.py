import pytest

from django.contrib import auth
from django.urls import reverse

from main_app.models import (
    Disease, DiseaseSymptom, GeographicalArea, 
    Organ, Symptom, Treatment, User
)


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


@pytest.mark.django_db
def test_contact_page_view(client):
    url = reverse('contact_page')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_page_send_message(client):
    url = reverse('contact_page')
    response = client.post(url, {
        'sender': 'Sender',
        'sender_email': 'test@gmail.com',
        'message': 'some message'
    })
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view(client, user):
    url = reverse('log_in')
    response = client.post(url, {
        'username': user.username, 
        'password': user.password
    })
    client.login(username=user.username, password=user.password)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client, user):
    url = reverse('logout')
    response = client.post(url, {'username': user.username})
    client.logout()
    assert response.status_code == 302


@pytest.mark.django_db
def test_change_data_view(client, user):
    url = reverse('change_data', args=[user.pk])
    response = client.post(url, {
        'first_name': 'New',
        'last_name': 'Name',
    })
    assert response.status_code == 302
