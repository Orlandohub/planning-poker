import os
from core.security import verify_password, get_password_hash

MOCK_PASSWORD = "secret"
MOCK_PASSWORD_HASH = "$2b$12$jHT0QwjqCTOxVpW.TNXoGOqHkzZsO.vg3k2LJdmUnp6uoiL9gHyEm"


def test_verify_password():
    assert verify_password(MOCK_PASSWORD, MOCK_PASSWORD_HASH) == True
