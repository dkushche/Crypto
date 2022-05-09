""" ms_cryptoapi_verify

Verify data signed with certificate

Parameters
----------
TODO

Returns
-------
TODO

"""

import platform
import string

import windows.crypto as crypto

import crypto_tools


def ms_cryptoapi_verify_little_doc():
    return "ms_cryptoapi_verify_little_doc"


def ms_cryptoapi_verify_full_doc():
    return """
    ms_cryptoapi_verify_full_doc
    """


def ms_cryptoapi_verify_processing(data: bytes, storage_loc: string, issuer: bytes, serial: str):
    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    storage = crypto_tools.ms_cryptoapi_get_storage(storage_loc)
    if storage is None:
        raise Exception(f"no such storage: {storage_loc}")

    try:
        for cert in storage.certs:
            if cert.issuer == issuer and cert.serial == serial:
                return crypto.verify_signature(cert, data)
        raise Exception('No such certificate')
    except:
        raise Exception('Not verified')


@crypto_tools.file_manipulation(save=False)
def ms_cryptoapi_verify(data: bytearray):
    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    storage_loc = crypto_tools.cterm('input', 'Enter storage location(str): ', 'ans')
    issuer = crypto_tools.cterm('input', 'Enter certificate issuer(str): ', 'ans')
    serial = crypto_tools.cterm('input', 'Enter certificate serial(str): ', 'ans')

    return ms_cryptoapi_verify_processing(
        data, storage_loc, issuer.encode(), serial
    )


ms_cryptoapi_verify.little_doc = ms_cryptoapi_verify_little_doc
ms_cryptoapi_verify.full_doc = ms_cryptoapi_verify_full_doc
ms_cryptoapi_verify.processor = ms_cryptoapi_verify_processing
