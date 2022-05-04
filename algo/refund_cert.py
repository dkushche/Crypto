""" refund_cert

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


def refund_cert_little_doc():
    return "refund_cert_little_doc"


def refund_cert_full_doc():
    return """
    refund_cert_full_doc
    """


def refund_cert_processing(username, list_name):
    client_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM,
        crypto_tools.download_text(f"storage/certs/{username}/{username}_cert.pem")
    )

    if not os.path.exists(f"storage/certs/revokes/{list_name}.crl"):
        raise ValueError("no such CRL")

    crl = crypto.load_crl(
        crypto.FILETYPE_PEM,
        crypto_tools.download_text(f"storage/certs/revokes/{list_name}.crl")
    )

    ca_key = crypto.load_privatekey(
        crypto.FILETYPE_PEM, crypto_tools.download_text("crypto_ca/crypto_key.pem")
    )

    crypto_crl = crl.to_cryptography()
    is_revoked = crypto_crl.get_revoked_certificate_by_serial_number(
        client_cert.get_serial_number()
    )

    if not is_revoked:
        raise ValueError("certificate isn't revoked")

    revocation_time = datetime.utcnow().strftime('%Y%m%d%H%M%SZ').encode()

    new_crl = crypto.CRL()
    new_crl.set_lastUpdate(revocation_time)

    revokes_list = crl.get_revoked()
    for i in range(len(revokes_list)):
        revoked_serial = int(revokes_list[i].get_serial().decode("utf-8"))
        if revoked_serial != client_cert.get_serial_number():
            new_crl.add_revoked(revokes_list[i])

    os.remove(f"storage/certs/revokes/{list_name}.crl")

    if new_crl.get_revoked() is not None:
        new_crl.sign(client_cert, ca_key, 'sha512'.encode())
        new_crl_pem = crypto.dump_crl(crypto.FILETYPE_PEM, new_crl)

        with open(f"storage/certs/revokes/{list_name}.crl", "wt") as pem:
            pem.write(new_crl_pem.decode('utf-8'))


def refund_cert():
    username = crypto_tools.cterm('input', 'Enter username(str): ', 'ans')
    list_name = crypto_tools.cterm('input', 'Enter list name(str): ', 'ans')

    refund_cert_processing(username, list_name)

    crypto_tools.cterm("output", "Refund Successfully!", "inf")


refund_cert.little_doc = refund_cert_little_doc
refund_cert.full_doc = refund_cert_full_doc
refund_cert.processor = refund_cert_processing
