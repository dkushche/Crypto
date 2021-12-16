import crypto_tools


def issue_cert_little_doc():
    return "issue_cert_little_doc"


def issue_cert_full_doc():
    return """
    issue_cert_full_doc
    """


def issue_cert_processing(data, key):
    return data


@crypto_tools.file_manipulation()
def issue_cert(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    return issue_cert_processing(data, key)


issue_cert.little_doc = issue_cert_little_doc
issue_cert.full_doc = issue_cert_full_doc
