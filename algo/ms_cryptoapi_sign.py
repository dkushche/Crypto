""" ms_cryptoapi_sign

Signs data using certificate

Parameters
----------
TODO

Returns
-------
TODO

"""

import platform

import windows.crypto as crypto

import crypto_tools


def ms_cryptoapi_sign_little_doc():
    return "ms_cryptoapi_sign_little_doc"


def ms_cryptoapi_sign_full_doc():
    return """
    ms_cryptoapi_sign_full_doc
    """


def ms_cryptoapi_sign_processing(data: bytearray, storage_loc: str, create_storage: bool, cert_name: str, serial: str) -> bytes:
    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    storage = crypto_tools.ms_cryptoapi_get_storage(storage_loc, create_storage)
    if serial is None:
        certif = crypto_tools.ms_cryptoapi_generate_cert(storage_loc, cert_name)
        storage.add_certificate(certif)
    else:
        for cert in storage.certs:
            if cert.issuer == cert_name and cert.serial == serial:
                certif = cert
                break

    return crypto.sign(certif, data), certif.issuer, certif.serial


@crypto_tools.file_manipulation()
def ms_cryptoapi_sign(data: bytearray):
    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    storage_loc = crypto_tools.cterm('input', 'Enter storage location(str): ', 'ans')
    create_storage = bool(crypto_tools.cterm('input', 'Do you want to create storage(1 `yes`|0 `no`):', 'ans'))
    cert_name = crypto_tools.cterm('input', 'Enter certificate name(str): ', 'ans')
    create_cert = bool(crypto_tools.cterm('input', 'Do you want to create certificate(1 `yes`|0 `no`):', 'ans'))

    serial = None
    if not create_cert:
        serial = crypto_tools.cterm('input', 'Enter certificate serial(str): ', 'ans')

    res, issuer, serial = ms_cryptoapi_sign_processing(data, storage_loc, create_storage, cert_name, serial)

    crypto_tools.cterm("output", f"Certificate issuer: {issuer}", "inf")
    crypto_tools.cterm("output", f"Certificate serial: {serial}", "inf")

    return res


ms_cryptoapi_sign.little_doc = ms_cryptoapi_sign_little_doc
ms_cryptoapi_sign.full_doc = ms_cryptoapi_sign_full_doc
ms_cryptoapi_sign.processor = ms_cryptoapi_sign_processing
