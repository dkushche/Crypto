""" revoke_cert tests

"""

import os
import shutil

import pytest

from OpenSSL import crypto

from algo import generate_ca
from algo import issue_cert
from algo import revoke_cert

from crypto_tools import download_text

TEST_USERNAME = "test_user"
TEST_REVOKE_LIST_NAME = "test_revoke"


@pytest.mark.standard_set
def test_revoke_cert_success():
    end_time = 365 * 24 * 60 * 60

    ca_cert_info = {
        "emailAddress": "test_ca@mail.com",
        "commonName": "test_ca_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "crypto_ca",
        "serialNumber": 1,
        "validityInSeconds": end_time,
    }

    generate_ca.processor(ca_cert_info)

    username = TEST_USERNAME
    client_cert_info = {
        "emailAddress": "test_user@mail.com",
        "commonName": "test_user_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "pytest_worker",
        "serialNumber": 2,
        "validityInSeconds": end_time,
    }

    issue_cert.processor(client_cert_info, None, username)

    revoke_cert.processor(username, TEST_REVOKE_LIST_NAME)

    assert os.path.exists(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl")

    crl = crypto.load_crl(
        crypto.FILETYPE_PEM, download_text(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl")
    )

    crl_crypto = crl.to_cryptography()
    ca_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, download_text("crypto_ca/crypto_cert.pem")
    )
    crl_crypto.is_signature_valid(ca_cert.get_pubkey().to_cryptography_key())

    client_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, download_text(f"storage/certs/{username}/{username}_cert.pem")
    )

    assert crl_crypto.get_revoked_certificate_by_serial_number(
        client_cert.get_serial_number()) is not None


@pytest.mark.standard_set
def test_revoke_cert_double():
    end_time = 365 * 24 * 60 * 60

    ca_cert_info = {
        "emailAddress": "test_ca@mail.com",
        "commonName": "test_ca_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "crypto_ca",
        "serialNumber": 1,
        "validityInSeconds": end_time,
    }

    generate_ca.processor(ca_cert_info)

    username = TEST_USERNAME
    client_cert_info = {
        "emailAddress": "test_user@mail.com",
        "commonName": "test_user_cert",
        "countryName": "ua",
        "localityName": "ua",
        "stateOrProvinceName": "Kyiv",
        "organizationName": "crypto_test",
        "organizationUnitName": "pytest_worker",
        "serialNumber": 2,
        "validityInSeconds": end_time,
    }

    issue_cert.processor(client_cert_info, None, username)

    revoke_cert.processor(username, TEST_REVOKE_LIST_NAME)
    with pytest.raises(ValueError) as revoke_err:
        revoke_cert.processor(username, TEST_REVOKE_LIST_NAME)
    assert revoke_err.value.args[0] == "certificate already revoked"


@pytest.fixture(autouse=True)
def revoke_cert_cleaner():
    yield

    shutil.rmtree("crypto_ca", ignore_errors=True)
    shutil.rmtree(f"storage/certs/{TEST_USERNAME}",  ignore_errors=True)

    if os.path.exists(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl"):
        os.remove(f"storage/certs/revokes/{TEST_REVOKE_LIST_NAME}.crl")
