import os
import sys

import pytest
from rest_framework.test import APIClient


sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client_api():
    client = APIClient()
    return client
