from traceback import print_tb
import pytest

from algo import caesar

@pytest.mark.standard_set
def test_caesar_success():
    assert "МПМ" == caesar.processor("ЛОЛ", "russian", 1)
