import crypto_tools


def cryptoapi_aes_little_doc():
    return "cryptoapi_aes_little_doc"


def cryptoapi_aes_full_doc():
    return """
    cryptoapi_aes_full_doc
    """


def cryptoapi_aes_processing(data, key):
    return data


@crypto_tools.file_manipulation()
def cryptoapi_aes(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    return cryptoapi_aes_processing(data, key)


cryptoapi_aes.little_doc = cryptoapi_aes_little_doc
cryptoapi_aes.full_doc = cryptoapi_aes_full_doc
