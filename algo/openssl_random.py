""" Random

Generating random sequence with specific length

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools
import crypto_native


def openssl_random_little_doc():
    return "openssl_random_little_doc"


def openssl_random_full_doc():
    return """
    openssl_random_full_doc
    """


def openssl_random_processing(length):
    crypto_native.openssl_api_init()

    result = crypto_native.openssl_api_random(length)

    return result


@crypto_tools.file_manipulation(read_data=False)
def openssl_random():
    length = int(crypto_tools.cterm('input', 'Enter sequence length(int): ', 'ans'))
    return openssl_random_processing(length)


openssl_random.little_doc = openssl_random_little_doc
openssl_random.full_doc = openssl_random_full_doc
