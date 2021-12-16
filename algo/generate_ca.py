import os
import shutil

import crypto_tools
import OpenSSL


def generate_ca_little_doc():
    return "generate_ca_little_doc"


def generate_ca_full_doc():
    return """
    generate_ca_full_doc
    """


def generate_ca_processing(ca_info):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    
    if os.path.exists("crypto_ca"):
        shutil.rmtree("crypto_ca")
    os.mkdir("crypto_ca")

    cert = crypto_tools.generate_cert(ca_info, ca_info, key, key)

    with open("crypto_ca/crypto_cert.pem", "wt") as f:
        f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert).decode("utf-8"))

    with open("crypto_ca/crypto_key.pem", "wt") as f:
        f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key).decode("utf-8"))

    pkcs12_cert = OpenSSL.crypto.PKCS12()
    pkcs12_cert.set_privatekey(key)
    pkcs12_cert.set_certificate(cert)

    p12data = pkcs12_cert.export("")
    with open('crypto_ca/crypto_pkcs12_cert.pfx', 'wb') as pfxfile:
        pfxfile.write(p12data)

    return "Created Successfully!"


def generate_ca():
    ca_cert_info = {
        "emailAddress": crypto_tools.cterm('input', 'Enter email(str): ', 'ans'),
        "commonName": crypto_tools.cterm('input', 'Enter common name(str): ', 'ans'),
        "countryName": crypto_tools.cterm('input', 'Enter country name(str): ', 'ans'),
        "localityName": crypto_tools.cterm('input', 'Enter locality name(str): ', 'ans'),
        "stateOrProvinceName": crypto_tools.cterm('input', 'Enter state or province name(str): ', 'ans'),
        "organizationName": crypto_tools.cterm('input', 'Enter organization name(str): ', 'ans'),
        "organizationUnitName": crypto_tools.cterm('input', 'Enter organization unit name(str): ', 'ans'),
        "serialNumber": int(crypto_tools.cterm('input', 'Enter serial number name(int): ', 'ans')),
        "validityEndInSeconds": int(crypto_tools.cterm('input', 'Enter validity end in seconds(int): ', 'ans')),
    }

    return generate_ca_processing(ca_cert_info)


generate_ca.little_doc = generate_ca_little_doc
generate_ca.full_doc = generate_ca_full_doc
