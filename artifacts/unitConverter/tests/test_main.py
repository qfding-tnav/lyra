import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import convert_area_value, main


def test_convert_area_value_delegates_successfully():
    assert convert_area_value(2, 'square_meter', 'square_centimeter') == 20000.0


def test_main_success_prints_result_and_returns_zero(capsys):
    exit_code = main(['2', 'square_meter', 'square_centimeter'])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == '20000.0'


def test_main_invalid_arity_prints_usage_and_returns_one(capsys):
    exit_code = main(['2', 'square_meter'])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert 'Usage:' in captured.out


def test_main_invalid_value_prints_error_and_returns_one(capsys):
    exit_code = main(['not-a-number', 'square_meter', 'square_centimeter'])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert 'Error:' in captured.out


def test_main_invalid_unit_prints_error_and_returns_one(capsys):
    exit_code = main(['2', 'bad_unit', 'square_centimeter'])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert 'Error:' in captured.out
    assert 'Unsupported area unit' in captured.out
