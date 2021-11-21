import crypto_tools
import ctypes


def openssl_api_little_doc():
    return "short example of encryption and decryption using openssl"


def openssl_api_full_doc():
    return """
    openssl_api_full_doc
    """


def openssl_api_processing(data, mode):
    openssl = ctypes.cdll.LoadLibrary("crypto_storage/libssl.so")

    if mode == "CBC":
        cipher = openssl.EVP_aes_128_cbc
    else:
        cipher = openssl.EVP_aes_128_cfb128

    # bio = openssl.BIO_new_file(b'storage/Hello.txt', b'rb')
    # print(bio)

    # data = ctypes.c_char_p(bytes(6))
    # res = openssl.BIO_read(bio, data, 5)

    # print(f"Res: {res}; data: {data.value}")

    return data


@crypto_tools.file_manipulation()
def openssl_api(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

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

    res_data = openssl_api_processing(data, mode)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


openssl_api.little_doc = openssl_api_little_doc
openssl_api.full_doc = openssl_api_full_doc
