import pytest


if __name__ == '__main__':
    from flask_redoc_test.test_flask_redoc import TestFlaskRedoc
    pytest.main(['--color=auto', '--no-cov', '-v'])
