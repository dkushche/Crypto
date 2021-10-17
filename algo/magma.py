import crypto_tools

def magma_little_doc():
    return "block algorithm ГОСТ 28147-89"


def magma_full_doc():
    return """
    https://spy-soft.net/magma-encryption/
    """


def magma_processing(data):
    # Make block function more abstract and use them here
    return data


@crypto_tools.file_manipulation()
def magma(data):

    return magma_processing(data)


magma.little_doc = magma_little_doc
magma.full_doc = magma_full_doc

