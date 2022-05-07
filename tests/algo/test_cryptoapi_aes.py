"""
CryptoAPI AES test

"""

import platform

import pytest

from algo import ms_cryptoapi_aes


@pytest.mark.windows_set
def test_ms_cryptoapi_aes_nextgen():
    res_data, hashed_key, session_key = ms_cryptoapi_aes.processor(
        bytearray("test", "utf-8"), 128, bytearray("test", "utf-8"), "CBC", "nextgen", "encrypt"
    )

    assert res_data != f"Unsupported on {platform.system()} platform"
    assert hashed_key != f"Unsupported on {platform.system()} platform"
    assert session_key != f"Unsupported on {platform.system()} platform"
