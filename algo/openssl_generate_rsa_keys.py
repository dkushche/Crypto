import crypto_tools
import crypto_native


def openssl_generate_rsa_keys_little_doc():
    return "openssl_generate_rsa_keys_little_doc"


def openssl_generate_rsa_keys_full_doc():
    return """
    openssl_generate_rsa_keys_full_doc
    """


def openssl_generate_rsa_keys_processing(key_length, exponent,
                                         pem_key_filename, pub_key_filename):
    crypto_native.openssl_api_init()

    result = crypto_native.openssl_api_generate_rsa_keys(
        key_length, exponent, pem_key_filename, pub_key_filename
    )

    crypto_tools.cterm("output", result, "inf")


def openssl_generate_rsa_keys():
    if not os.path.exists("storage/"):
        os.mkdir("storage/")

    key_length = int(crypto_tools.cterm('input', 'Enter key legth(int): ', 'ans'))
    exponent = int(crypto_tools.cterm('input', 'Enter exponent(int): ', 'ans'))

    pem_key_filename = crypto_tools.cterm('input', 'Enter private key filename(str): ', 'ans')
    pem_key_filename = "storage/" + pem_key_filename

    pub_key_filename = crypto_tools.cterm('input', 'Enter public key filename(str): ', 'ans')
    pub_key_filename = "storage/" + pub_key_filename

    return openssl_generate_rsa_keys_processing(
        key_length, exponent, pem_key_filename, pub_key_filename
    )


openssl_generate_rsa_keys.little_doc = openssl_generate_rsa_keys_little_doc
openssl_generate_rsa_keys.full_doc = openssl_generate_rsa_keys_full_doc
