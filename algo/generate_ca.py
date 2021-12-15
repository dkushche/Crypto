import crypto_tools
import crypto_native


def generate_ca_little_doc():
    return "generate_ca_little_doc"


def generate_ca_full_doc():
    return """
    generate_ca_full_doc
    """


def generate_ca_processing(data, key):
    return data


@crypto_tools.file_manipulation()
def generate_ca(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')


    return generate_ca_processing(data, key)


generate_ca.little_doc = generate_ca_little_doc
generate_ca.full_doc = generate_ca_full_doc
