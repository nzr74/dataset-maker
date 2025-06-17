import sys
import pytest
from unittest import mock
import main

@pytest.fixture(autouse=True)
def reset_argv():
    original_argv = sys.argv.copy()
    yield
    sys.argv = original_argv

def test_no_arguments(capsys):
    sys.argv = ["main.py"]
    main.main()
    captured = capsys.readouterr()
    assert "please insert site and category" in captured.out

def test_invalid_site(capsys):
    sys.argv = ["main.py", "--s", "unknown", "--c", "car"]
    main.main()
    captured = capsys.readouterr()
    assert "please insert correct site" in captured.out

def test_bama_car_calls_extract_car_data(monkeypatch):
    sys.argv = ["main.py", "--s", "bama", "--c", "car"]
    called = {}

    class DummyBama:
        def __init__(self, category, missing_value):
            called['init'] = (category, missing_value)
        def extract_car_data(self):
            called['extract'] = True

    monkeypatch.setattr(main, "Bama", DummyBama)
    main.main()
    assert called['init'] == ("car", "False") or called['init'] == ("car", False)
    assert called['extract'] is True

def test_divar_car_calls_extract_car_data(monkeypatch):
    sys.argv = ["main.py", "--s", "divar", "--c", "car"]
    called = {}

    class DummyDivar:
        def __init__(self, category, missing_value):
            called['init'] = (category, missing_value)
        def extract_car_data(self):
            called['extract'] = True

    monkeypatch.setattr(main, "Divar", DummyDivar)
    main.main()
    assert called['init'] == ("car", "False") or called['init'] == ("car", False)
    assert called['extract'] is True

def test_bama_non_car(monkeypatch):
    sys.argv = ["main.py", "--s", "bama", "--c", "house"]
    called = {}

    class DummyBama:
        def __init__(self, category, missing_value):
            called['init'] = (category, missing_value)
        def extract_car_data(self):
            called['extract'] = True

    monkeypatch.setattr(main, "Bama", DummyBama)
    main.main()
    assert called['init'] == ("house", "False") or called['init'] == ("house", False)
    assert 'extract' not in called

def test_divar_non_car(monkeypatch):
    sys.argv = ["main.py", "--s", "divar", "--c", "house"]
    called = {}

    class DummyDivar:
        def __init__(self, category, missing_value):
            called['init'] = (category, missing_value)
        def extract_car_data(self):
            called['extract'] = True

    monkeypatch.setattr(main, "Divar", DummyDivar)
    main.main()
    assert called['init'] == ("house", "False") or called['init'] == ("house", False)
    assert 'extract' not in called

def test_sheypoor_and_esam_do_nothing(capsys):
    sys.argv = ["main.py", "--s", "sheypoor", "--c", "car"]
    main.main()
    captured = capsys.readouterr()
    assert captured.out == ""

    sys.argv = ["main.py", "--s", "esam", "--c", "car"]
    main.main()
    captured = capsys.readouterr()
    assert captured.out == ""

def test_missing_value_argument(monkeypatch):
    sys.argv = ["main.py", "--s", "bama", "--c", "car", "--mv", "True"]
    called = {}

    class DummyBama:
        def __init__(self, category, missing_value):
            called['init'] = (category, missing_value)
        def extract_car_data(self):
            called['extract'] = True

    monkeypatch.setattr(main, "Bama", DummyBama)
    main.main()
    assert called['init'] == ("car", "True")
    assert called['extract'] is True