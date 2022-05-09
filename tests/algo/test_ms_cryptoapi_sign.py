""" ms_cryptoapi_sign tests

"""

import pytest

from algo import ms_cryptoapi_sign

@pytest.mark.windows_set
def test_ms_cryptoapi_sign_success():
    ms_cryptoapi_sign.processor(
        bytearray("dima_kushchevskyi".encode()), "MAIN", False, "test_kushchevskyi", None
    )
