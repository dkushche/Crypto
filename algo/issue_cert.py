""" Issue cert

Issue ssl certificate. Before using this command
generate CA firstly.

Parameters
----------
TODO

Returns
-------
TODO

"""

import os
import shutil
import OpenSSL

import crypto_tools


def issue_cert_little_doc():
    return "issue_cert_little_doc"


def issue_cert_full_doc():
    return """
    issue_cert_full_doc
    """


def issue_cert_processing(cert_info, username):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    if not os.path.exists("crypto_ca"):
        raise Exception("Generate CA firstly")

    if os.path.exists(f"storage/certs/{username}"):
        shutil.rmtree(f"storage/certs/{username}")
    os.makedirs(f"storage/certs/{username}")

    ca_cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, crypto_tools.download_text("crypto_ca/crypto_cert.pem")
    )
    ca_key = OpenSSL.crypto.load_privatekey(
        OpenSSL.crypto.FILETYPE_PEM, crypto_tools.download_text("crypto_ca/crypto_key.pem")
    )

    cert = crypto_tools.generate_cert(cert_info, key, ca_key, ca_cert.get_subject())

    with open(f"storage/certs/{username}/{username}_cert.pem", "wt") as pem:
        pem.write(OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert).decode("utf-8")
        )

    with open(f"storage/certs/{username}/{username}_key.pem", "wt") as pem:
        pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key).decode("utf-8"))

    pkcs12_cert = OpenSSL.crypto.PKCS12()
    pkcs12_cert.set_privatekey(key)
    pkcs12_cert.set_certificate(cert)

    p12data = pkcs12_cert.export(b"")
    with open(f"storage/certs/{username}/{username}_pkcs12_cert.pfx", 'wb') as pfxfile:
        pfxfile.write(p12data)


def issue_cert():
    cert_info = {
        "emailAddress": crypto_tools.cterm('input', 'Enter email(str): ', 'ans'),
        "commonName": crypto_tools.cterm('input', 'Enter common name(str): ', 'ans'),
        "countryName": crypto_tools.cterm('input', 'Enter country name(str): ', 'ans'),
        "localityName": crypto_tools.cterm('input', 'Enter locality name(str): ', 'ans'),
        "stateOrProvinceName": crypto_tools.cterm(
            'input', 'Enter state or province name(str): ', 'ans'
        ),
        "organizationName": crypto_tools.cterm(
            'input', 'Enter organization name(str): ', 'ans'
        ),
        "organizationUnitName": crypto_tools.cterm(
            'input', 'Enter organization unit name(str): ', 'ans'
        ),
        "serialNumber": int(crypto_tools.cterm(
            'input', 'Enter serial number(int): ', 'ans'
        )),
        "validityInSeconds": int(crypto_tools.cterm(
            'input', 'Enter validity in seconds(int): ', 'ans'
        )),
    }
    username = crypto_tools.cterm('input', 'Enter username(str): ', 'ans')

    issue_cert_processing(cert_info, username)
    crypto_tools.cterm("output", "Issued Successfully!", "inf")


issue_cert.little_doc = issue_cert_little_doc
issue_cert.full_doc = issue_cert_full_doc
issue_cert.processor = issue_cert_processing
