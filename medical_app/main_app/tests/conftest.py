import os
import sys

import pytest

from django.test import Client


sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    """Return created Client object."""
    return Client()
