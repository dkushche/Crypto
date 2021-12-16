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
#     "validityEndInSeconds":
# }
def generate_cert(cert_info, issuer_info, pub_key, signing_key):
    cert = OpenSSL.crypto.X509()

    cert_subject = cert.get_subject()
    cert_subject.C = cert_info["countryName"]
    cert_subject.ST = cert_info["stateOrProvinceName"]
    cert_subject.L = cert_info["localityName"]
    cert_subject.O = cert_info["organizationName"]
    cert_subject.OU = cert_info["organizationUnitName"]
    cert_subject.CN = cert_info["commonName"]
    cert_subject.emailAddress = cert_info["emailAddress"]

    issuer = OpenSSL.crypto.X509()

    issuer_subject = issuer.get_subject()
    issuer_subject.C = issuer_info["countryName"]
    issuer_subject.ST = issuer_info["stateOrProvinceName"]
    issuer_subject.L = issuer_info["localityName"]
    issuer_subject.O = issuer_info["organizationName"]
    issuer_subject.OU = issuer_info["organizationUnitName"]
    issuer_subject.CN = issuer_info["commonName"]
    issuer_subject.emailAddress = issuer_info["emailAddress"]

    cert.set_serial_number(cert_info["serialNumber"])

    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(cert_info["validityEndInSeconds"])

    cert.set_issuer(issuer_subject)

    cert.set_pubkey(pub_key)
    cert.sign(signing_key, 'sha512')

    return cert
