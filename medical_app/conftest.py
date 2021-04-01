import pytest

from django.test import Client


@pytest.fixture
def client():
    """Return created Client object."""
    return Client()

