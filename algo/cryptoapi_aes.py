import crypto_tools
import crypto_native

def cryptoapi_aes_little_doc():
    return "cryptoapi_aes_little_doc"


def cryptoapi_aes_full_doc():
    return """
    cryptoapi_aes_full_doc
    """


def cryptoapi_aes_pre_processing(key, key_length):
    if len(key) > key_length //  8:
        raise ValueError(f"Too big key. Max len required: {key_length //  8}")
    else:
        crypto_tools.supl_to_mult(key, key_length //  8)


def cryptoapi_aes_processing(data, key_length, key,
                            mode, provider, encrypt):
    cryptoapi_aes_pre_processing(key, key_length)

    if provider == "standard":
        result = crypto_native.ms_cryptoapi_standard_aes(
            data, key, encrypt
        )
    else:
        result = crypto_native.ms_cryptoapi_nextgen_aes(
            data, key, mode, encrypt
        )

    crypto_tools.cterm("output", f"Hashed key: {result['hashed_key']}", "inf")
    crypto_tools.cterm("output", f"Session key: {result['session_key']}", "inf")

    return result["result"]


@crypto_tools.file_manipulation()
def cryptoapi_aes(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    key_length = crypto_tools.cterm('input', 'Enter key length(128|192|256)bit: ', 'ans')
    if key_length not in ["128", "192", "256"]:
        raise ValueError(f"Incorrect key length: {key_length}")
    key_length = int(key_length)

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    provider = crypto_tools.cterm('input', 'Enter provider(standard|nextgen): ', 'ans')
    if provider not in ["standard", "nextgen"]:
        raise ValueError(f"Incorrect provider: {provider}")

    mode = None
    if provider == "nextgen":
        mode = crypto_tools.cterm('input', 'Enter mode(CBC|ECB|CFB): ', 'ans')
        if mode not in ["CBC", "ECB", "CFB"]:
            raise ValueError(f"Incorrect mode: {mode}")
    
    encrypt = crypto_tools.cterm('input', 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ["decrypt", "encrypt"]:
        raise ValueError("Incorrect type")

    res_data = cryptoapi_aes_processing(data, key_length, key,
                                        mode, provider, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


cryptoapi_aes.little_doc = cryptoapi_aes_little_doc
cryptoapi_aes.full_doc = cryptoapi_aes_full_doc
