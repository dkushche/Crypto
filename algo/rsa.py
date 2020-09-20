import crypto_tools


def rsa_little_doc():
    return "encrypt/decrypt using rsa algo"


def rsa_full_doc():
    return """
    
    """


def rsa_processing(data, input_val):
    return result


@crypto_tools.file_manipulation
def rsa(data):
    input_val = int(crypto_tools.cterm('input','data', 'ans'))
    return hash_processing(data, input_val)


rsa.little_doc = rsa_little_doc
rsa.full_doc = rsa_full_doc
