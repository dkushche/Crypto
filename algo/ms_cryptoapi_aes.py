""" CryptoAPI AES

Advanced Encryption Standard encryption using
Microsoft CryptoAPI native library

Parameters
----------
TODO

Returns
-------
TODO

"""

import platform
import crypto_tools

def ms_cryptoapi_aes_little_doc():
    return "ms_cryptoapi_aes_little_doc"


def ms_cryptoapi_aes_full_doc():
    return """
    ms_cryptoapi_aes_full_doc
    """


def ms_cryptoapi_aes_pre_processing(key, key_length):
    if len(key) > key_length //  8:
        raise ValueError(f"Too big key. Max len required: {key_length //  8}")

    crypto_tools.supl_to_mult(key, key_length //  8)


def ms_cryptoapi_aes_processing(data, key_length, key,
                            mode, provider, encrypt):

    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    ms_cryptoapi_aes_pre_processing(key, key_length)

    if provider == "standard":
        (res_data, hashed_key, session_key) = crypto_tools.ms_cryptoapi_standard_aes(
            data, key, encrypt
        )
    else:
        (res_data, hashed_key, session_key) = crypto_tools.ms_cryptoapi_nextgen_aes(
            data, key, mode, encrypt
        )

    return (res_data, hashed_key, session_key)


@crypto_tools.file_manipulation()
def ms_cryptoapi_aes(data: bytearray):
    if platform.system() != "Windows":
        raise Exception(f"Unsupported on {platform.system()} platform")

    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    key_length = crypto_tools.cterm('input', 'Enter key length(128|192|256)bit: ', 'ans')
    if key_length not in ["128", "192", "256"]:
        raise ValueError(f"Incorrect key length: {key_length}")
    key_length = int(key_length)

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    provider = crypto_tools.cterm('input', 'Enter provider(standard|nextgen): ', 'ans')
    if provider not in ["standard", "nextgen"]:
        raise ValueError(f"Incorrect provider: {provider}")

    mode = None
    if provider == "nextgen":
        mode = crypto_tools.cterm('input', 'Enter mode(CBC|ECB|CFB): ', 'ans')
        if mode not in ["CBC", "ECB", "CFB"]:
            raise ValueError(f"Incorrect mode: {mode}")

    encrypt = crypto_tools.cterm('input', 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    (res_data, hashed_key, session_key) = ms_cryptoapi_aes_processing(
        data, key_length, key, mode, provider, encrypt)

    crypto_tools.cterm("output", f"Hashed key: {hashed_key}", "inf")
    crypto_tools.cterm("output", f"Session key: {session_key}", "inf")

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


ms_cryptoapi_aes.little_doc = ms_cryptoapi_aes_little_doc
ms_cryptoapi_aes.full_doc = ms_cryptoapi_aes_full_doc
ms_cryptoapi_aes.processor = ms_cryptoapi_aes_processing
