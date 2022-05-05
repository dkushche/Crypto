""" Cert tools

Set of tools for dealing with ssl certificates

"""

import time
import OpenSSL

# *_info = {
#     "emailAddress":
#     "commonName":
#     "countryName":
#     "localityName":
#     "stateOrProvinceName":
#     "organizationName":
#     "organizationUnitName":
#     "serialNumber":
#     "validityInSeconds":
# }
def generate_cert(cert_info, extensions, pub_key, signing_key, issuer_subject=None):
    cert = OpenSSL.crypto.X509()

    cert_subject = cert.get_subject()
    cert_subject.C = cert_info["countryName"]
    cert_subject.ST = cert_info["stateOrProvinceName"]
    cert_subject.L = cert_info["localityName"]
    cert_subject.O = cert_info["organizationName"]
    cert_subject.OU = cert_info["organizationUnitName"]
    cert_subject.CN = cert_info["commonName"]
    cert_subject.emailAddress = cert_info["emailAddress"]

    if issuer_subject is not None:
        cert.set_issuer(issuer_subject)
    else:
        cert.set_issuer(cert_subject)

    cert.set_serial_number(cert_info["serialNumber"])

    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(int(time.time()) + cert_info["validityInSeconds"])

    if extensions is not None:
        exts = []

        for extension in extensions:
            ext = OpenSSL.crypto.X509Extension(
                extension["type"],
                extension["crytical"],
                extension["value"]
            )
            exts.append(ext)

        cert.add_extensions(exts)

    cert.set_pubkey(pub_key)
    cert.sign(signing_key, 'sha512')

    return cert
