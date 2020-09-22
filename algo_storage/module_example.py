import crypto_tools


def module_little_doc():
    return "little_doc"


def module_full_doc():
    return """
    full_doc
    """


def module_processing(data, input_val):
    return result


@crypto_tools.file_manipulation
def module(data):
    input_val = int(crypto_tools.cterm('input', 'data', 'ans'))
    return module_processing(data, input_val)


module.little_doc = module_little_doc
module.full_doc = module_full_doc
