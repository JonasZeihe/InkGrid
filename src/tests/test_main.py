"""
Tests for the main entry point of InkGrid.
"""

import sys
import pytest
from app.main import main, parse_command_line_arguments


def dummy_run_app(logging_enabled=False):
    """
    Returns a dummy output directory without starting the GUI.
    """
    return "dummy_output_dir"


def dummy_finalize_file_logging(logger, output_dir):
    """
    Dummy finalize function that does nothing.
    """
    pass


def dummy_run_app_exception(logging_enabled=False):
    """
    Raises an exception to simulate a failure in run_app.
    """
    raise Exception("Dummy error")


def test_parse_command_line_arguments_default(monkeypatch):
    """
    Tests that parse_command_line_arguments returns default values when no flags are provided.
    """
    monkeypatch.setattr(sys, "argv", ["main.py"])
    args = parse_command_line_arguments()
    assert not args.logging


def test_parse_command_line_arguments_logging(monkeypatch):
    """
    Tests that the --logging flag is correctly recognized.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--logging"])
    args = parse_command_line_arguments()
    assert args.logging


def test_main_without_logging(monkeypatch):
    """
    Tests the normal execution of main() without logging enabled.
    Replaces run_app in app.main with a dummy function so that no GUI is launched.
    Also ensures finalize_file_logging is not called.
    """
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setattr("app.main.run_app", dummy_run_app)
    finalize_called = False

    def fake_finalize(logger, output_dir):
        nonlocal finalize_called
        finalize_called = True

    monkeypatch.setattr("app.logger_config.finalize_file_logging", fake_finalize)
    monkeypatch.setattr("app.main.finalize_file_logging", fake_finalize)
    main()
    assert not finalize_called


def test_main_with_logging(monkeypatch):
    """
    Tests the execution of main() with logging enabled.
    Replaces run_app in app.main with a dummy function and verifies that finalize_file_logging is called.
    """
    monkeypatch.setattr(sys, "argv", ["main.py", "--logging"])
    monkeypatch.setattr("app.main.run_app", dummy_run_app)
    finalize_called = False

    def fake_finalize(logger, output_dir):
        nonlocal finalize_called
        finalize_called = True

    monkeypatch.setattr("app.logger_config.finalize_file_logging", fake_finalize)
    monkeypatch.setattr("app.main.finalize_file_logging", fake_finalize)
    main()
    assert finalize_called


def test_main_exception(monkeypatch):
    """
    Tests that main() exits with code 1 when run_app raises an exception.
    """
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setattr("app.main.run_app", dummy_run_app_exception)
    monkeypatch.setattr(
        "app.logger_config.finalize_file_logging", dummy_finalize_file_logging
    )
    monkeypatch.setattr("app.main.finalize_file_logging", dummy_finalize_file_logging)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
