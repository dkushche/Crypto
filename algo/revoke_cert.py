""" revoke_cert

TODO

Parameters
----------
TODO

Returns
-------
TODO

"""

import os
from datetime import datetime

from OpenSSL import crypto

import crypto_tools


def revoke_cert_little_doc():
    return "revoke_cert_little_doc"


def revoke_cert_full_doc():
    return """
    revoke_cert_full_doc
    """


def revoke_cert_processing(username, list_name):
    client_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM,
        crypto_tools.download_text(f"storage/certs/{username}/{username}_cert.pem")
    )

    if os.path.exists(f"storage/certs/revokes/{list_name}.crl"):
        crl = crypto.load_crl(
            crypto.FILETYPE_PEM,
            crypto_tools.download_text(f"storage/certs/revokes/{list_name}.crl")
        )

        crypto_crl = crl.to_cryptography()
        is_revoked = crypto_crl.get_revoked_certificate_by_serial_number(
            client_cert.get_serial_number()
        )

        if is_revoked:
            raise ValueError("certificate already revoked")
    else:
        if not os.path.exists("storage/certs/revokes"):
            os.makedirs("storage/certs/revokes")
        crl = crypto.CRL()

    ca_key = crypto.load_privatekey(
        crypto.FILETYPE_PEM, crypto_tools.download_text("crypto_ca/crypto_key.pem")
    )

    revocation_time = datetime.utcnow().strftime('%Y%m%d%H%M%SZ').encode()

    crl.set_lastUpdate(revocation_time)

    revoked = crypto.Revoked()
    revoked.set_serial(hex(client_cert.get_serial_number())[2:].encode())
    revoked.set_rev_date(revocation_time)
    revoked.set_reason(None)

    crl.add_revoked(revoked)
    crl.sign(client_cert, ca_key, 'sha512'.encode())

    crl_pem = crypto.dump_crl(crypto.FILETYPE_PEM, crl)

    with open(f"storage/certs/revokes/{list_name}.crl", "wt") as pem:
        pem.write(crl_pem.decode('utf-8'))


def revoke_cert():
    username = crypto_tools.cterm('input', 'Enter user name(str): ', 'ans')
    list_name = crypto_tools.cterm('input', 'Enter list name(str): ', 'ans')

    revoke_cert_processing(username, list_name)

    crypto_tools.cterm("output", "Revoke Successfully!", "inf")


revoke_cert.little_doc = revoke_cert_little_doc
revoke_cert.full_doc = revoke_cert_full_doc
revoke_cert.processor = revoke_cert_processing
