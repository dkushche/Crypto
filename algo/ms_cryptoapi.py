import crypto_tools


def ms_cryptoapi_little_doc():
    return "ms_cryptoapi_little_doc"


def ms_cryptoapi_full_doc():
    return """
    ms_cryptoapi_full_doc
    """


def ms_cryptoapi_processing(data, key):
    return data


@crypto_tools.file_manipulation()
def ms_cryptoapi(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    return ms_cryptoapi_processing(data, key)


ms_cryptoapi.little_doc = ms_cryptoapi_little_doc
ms_cryptoapi.full_doc = ms_cryptoapi_full_doc

