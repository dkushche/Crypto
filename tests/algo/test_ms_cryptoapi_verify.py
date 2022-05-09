""" ms_cryptoapi_verify tests

"""

import pytest

from algo import ms_cryptoapi_sign
from algo import ms_cryptoapi_verify

@pytest.mark.windows_set
def test_ms_cryptoapi_verify_success():
    signed_data, issuer, serial = ms_cryptoapi_sign.processor(
        bytearray("dima_kushchevskyi".encode()), "MAIN", False, "test_kushchevskyi", None
    )

    ms_cryptoapi_verify.processor(signed_data, "MAIN", issuer, serial)
