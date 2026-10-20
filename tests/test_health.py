from health_utils import is_healthy


def test_success_status_code():
    assert is_healthy(200) is True


def test_error_status_code():
    assert is_healthy(500) is False