"""
CryptoAPI AES test

"""

import platform

import pytest

from algo import cryptoapi_aes


@pytest.mark.windows_set
def test_cryptoapi_aes_success():
    assert cryptoapi_aes.processor(
        bytearray("test", "utf-8"), 128, bytearray("test", "utf-8"), "CBC", "nextgen", "encrypt"
    ) != f"Unsupported on {platform.system()} platform"
