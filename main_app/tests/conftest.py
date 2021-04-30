import os
import sys

import pytest

from django.test import Client

from main_app.models import User


sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    """Return created Client object."""
    return Client()


@pytest.fixture 
def user():
    """Return created User object."""
    user = User.objects.create_user(
        first_name='First Name',
        last_name='Last Name',
        username='Username',
        password='password2021',
        email='email@gmail.com',
        medical_license=True
    )
    return user
