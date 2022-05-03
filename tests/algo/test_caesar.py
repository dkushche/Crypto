"""
Caesar algorithm tests

"""

import pytest

from algo import caesar


@pytest.mark.standard_set
def test_caesar_success():
    assert caesar.processor("ЛОЛ", "russian", 1) == "МПМ"
