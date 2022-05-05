"""
Client certs tests

"""

import os
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

    issue_cert.processor(client_cert_info, None, username)

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


@pytest.mark.standard_set
def test_issue_cert_extension():
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

    client_cert_exts = [
        {
            "type": b'nsCertType',
            "crytical": False,
            "value": b"server",
            "str": "SSL Server"
        },
        {
            "type": b"subjectAltName",
            "crytical": True,
            "value": b"IP:192.168.88.47",
            "str": "IP Address:192.168.88.47"
        }
    ]

    issue_cert.processor(client_cert_info, client_cert_exts, username)

    assert os.path.exists(f"storage/certs/{username}")
    assert os.path.exists(f"storage/certs/{username}/{username}_cert.pem")
    assert os.path.exists(f"storage/certs/{username}/{username}_key.pem")
    assert os.path.exists(f"storage/certs/{username}/{username}_pkcs12_cert.pfx")

    client_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, download_text(f'storage/certs/{username}/{username}_cert.pem')
    )

    assert client_cert.get_extension_count() == 2

    for i in range(2):
        ext = client_cert.get_extension(i)
        found = False
        for client_cert_ext in client_cert_exts:
            if str(ext) == client_cert_ext["str"]:
                found = True
                break

        assert found, f"{ext}"


@pytest.fixture(autouse=True)
def issue_cert_cleaner():
    yield

    shutil.rmtree("crypto_ca", ignore_errors=True)
    shutil.rmtree(f"storage/certs/{TEST_USERNAME}",  ignore_errors=True)
