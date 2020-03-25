from .file_manager import download_json, download_text
from .lang_tools import utf_decoder

def render_static(file):
    header = download_text("iface_storage/crypto." + file)
    if header:
        crypto_term("output", utf_decoder(header), "inf")
    else:
        header = "You may add custom in crypto" + file + " file"
        crypto_term("output", header, "inf")


def crypto_term(com_type, message, message_type):
    """
        com_type - does it input or output
        message - the text
        message_type - type from iface.json
    """
    begin = crypto_term.iface["colors"][crypto_term.iface["pallete"][message_type]]
    marker = crypto_term.iface["markers"][message_type]
    res_line = "{0}{1}{2}".format(begin, marker, message)
    if com_type == "input":
        res_line += crypto_term.iface["colors"][crypto_term.iface["pallete"]["def"]]
        return input(res_line)
    print(res_line)
try:
    crypto_term.iface = download_json("iface_storage/iface.json")
except FileNotFoundError:
    exit()
