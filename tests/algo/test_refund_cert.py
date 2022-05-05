""" refund_cert tests

"""

import os
import shutil

import pytest

from algo import generate_ca
from algo import issue_cert
from algo import revoke_cert
from algo import refund_cert

TEST_USERNAME = "test_user"
TEST_REVOKE_LIST_NAME = "test_revoke"


@pytest.mark.standard_set
def test_refund_cert_success():
    end_time = 365 * 24 * 60 * 60

    generate_ca.processor({
        "emailAddress": "test_ca@mail.com",
        "commonName": "test_ca_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "crypto_ca",
        "serialNumber": 1,
        "validityInSeconds": end_time,
    })

    issue_cert.processor({
        "emailAddress": "test_user@mail.com",
        "commonName": "test_user_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "pytest_worker",
        "serialNumber": 2,
        "validityInSeconds": end_time,
    }, None, TEST_USERNAME)

    revoke_cert.processor(TEST_USERNAME, TEST_REVOKE_LIST_NAME)

    refund_cert.processor(TEST_USERNAME, TEST_REVOKE_LIST_NAME)

    assert not os.path.exists(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl")


@pytest.fixture(autouse=True)
def revoke_cert_cleaner():
    yield

    shutil.rmtree("crypto_ca", ignore_errors=True)
    shutil.rmtree(f"storage/certs/{TEST_USERNAME}",  ignore_errors=True)

    if os.path.exists(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl"):
        os.remove(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl")
