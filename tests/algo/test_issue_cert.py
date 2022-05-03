"""
Client certs tests

"""

import os
import time
import shutil

import pytest

import OpenSSL

from algo import generate_ca
from algo import issue_cert

from crypto_tools import download_text

TEST_USERNAME = "test_user"


@pytest.mark.standard_set
def test_issue_cert_success():
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

    issue_cert.processor(client_cert_info, username)

    assert os.path.exists(f"storage/certs/{username}")
    assert os.path.exists(f"storage/certs/{username}/{username}_cert.pem")
    assert os.path.exists(f"storage/certs/{username}/{username}_key.pem")
    assert os.path.exists(f"storage/certs/{username}/{username}_pkcs12_cert.pfx")

    client_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, download_text(f'storage/certs/{username}/{username}_cert.pem')
    )

    root_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, download_text('crypto_ca/crypto_cert.pem')
    )

    store = OpenSSL.crypto.X509Store()
    store.add_cert(root_cert)

    ctx = OpenSSL.crypto.X509StoreContext(store, client_cert)
    ctx.verify_certificate()


@pytest.fixture(autouse=True)
def issue_cert_cleaner():
    yield

    shutil.rmtree("crypto_ca", ignore_errors=True)
    shutil.rmtree(f"storage/certs/{TEST_USERNAME}",  ignore_errors=True)
