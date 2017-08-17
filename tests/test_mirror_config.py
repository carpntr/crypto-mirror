import pytest
from util import *
import unittest
from unittest import mock


# Crappy test
# ToDO: Go lookup autouse fixtures

def test_call_darksky(monkeypatch):
    class MockRequests:
        def __init__(self, url):
            self.status_code = 200
    monkeypatch.setattr(requests, 'get', MockRequests)
    resp = darksky_call('token', 200)
    assert resp == True
    assert darksky_call('anotha_one', '202') == False
