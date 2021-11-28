import ctypes


class crypto_bytearray(ctypes.Structure):
    _fields_ = [("data", ctypes.c_void_p),
                ("len", ctypes.c_size_t)]


def to_crypto_bytearray(ba):
    return crypto_bytearray(
        data=ctypes.cast(ctypes.pointer(ba), ctypes.c_void_p),
        len=len(ba)
    )

def form_crypto_native_buffer(data):
    result = (ctypes.c_byte * len(data))
    if data.__class__ == str:
        result = result.from_buffer(bytearray(data, "utf-8"))
    else:
        result = result.from_buffer(bytearray(data))

    return result
