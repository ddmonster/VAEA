from fastapi.testclient import TestClient
import pytest
from VAEA.app import create_app
import sys

client = TestClient(create_app())



def test_static_file():
    print(sys.path)
    client.get("/static/index.html")
