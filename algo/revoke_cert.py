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
    if os.path.exists(f"storage/certs/revokes/{list_name}.crl"):
        crl = crypto.load_crl(
            crypto.FILETYPE_PEM,
            crypto_tools.download_text(f"storage/certs/revokes/{list_name}.crl")
        )
    else:
        if not os.path.exists("storage/certs/revokes"):
            os.makedirs("storage/certs/revokes")
        crl = crypto.CRL()

    client_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM,
        crypto_tools.download_text(f"storage/certs/{username}/{username}_cert.pem")
    )
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
    username = crypto_tools.cterm('input', 'Enter username(str): ', 'ans')
    list_name = crypto_tools.cterm('input', 'Enter certname(str): ', 'ans')

    return revoke_cert_processing(username, list_name)


revoke_cert.little_doc = revoke_cert_little_doc
revoke_cert.full_doc = revoke_cert_full_doc
revoke_cert.processor = revoke_cert_processing
