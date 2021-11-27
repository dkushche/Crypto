import crypto_tools
import crypto_native
import ctypes


def openssl_api_little_doc():
    return "short example of encryption and decryption using openssl"


def openssl_api_full_doc():
    return """
    openssl_api_full_doc
    """


def openssl_api_processing(data, key, iv, mode, encrypt):
    crypto_native.openssl_api_init()
    crypto_native.openssl_api_aes_128(data, key, iv, mode, encrypt)

    return data


@crypto_tools.file_manipulation()
def openssl_api(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    iv = crypto_tools.cterm('input', 'Enter initialization vector(str): ', 'ans')
    if iv.__class__ == str:
        iv = bytearray(iv.encode())

    mode = crypto_tools.cterm(
        'input',
        'Enter mode(CBC(Cipher Block Chaining)|CFB(Cipher Feedback)): ',
        'ans'
    )
    if mode not in ["CBC", "CFB"]:
        raise ValueError(f"Incorrect mode: {mode}")

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ["decrypt", "encrypt"]:
        raise ValueError("Incorrect type")

    res_data = openssl_api_processing(data, key, iv, mode, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


openssl_api.little_doc = openssl_api_little_doc
openssl_api.full_doc = openssl_api_full_doc
