import crypto_tools


def triple_des_little_doc():
    return "triple_des_little_doc"


def triple_des_full_doc():
    return """
    triple_des_full_doc
    """


def triple_des_processing(data, input_val):
    return data


@crypto_tools.file_manipulation()
def triple_des(data):
    input_val = int(crypto_tools.cterm('input', 'data for triple_des: ', 'ans'))
    return triple_des_processing(data, input_val)


triple_des.little_doc = triple_des_little_doc
triple_des.full_doc = triple_des_full_doc

