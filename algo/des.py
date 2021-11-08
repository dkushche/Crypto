import crypto_tools


def des_little_doc():
    return "des_little_doc"


def des_full_doc():
    return """
    des_full_doc
    """


def des_processing(data, input_val):
    return data


@crypto_tools.file_manipulation()
def des(data):
    input_val = int(crypto_tools.cterm('input', 'data for des: ', 'ans'))
    return des_processing(data, input_val)


des.little_doc = des_little_doc
des.full_doc = des_full_doc

