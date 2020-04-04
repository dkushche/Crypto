from .file_manager import download_json, download_text
from .lang_tools import utf_decoder


def render_static(file):
    header = download_text("iface_storage/crypto." + file)
    if header:
        cterm("output", utf_decoder(header), "inf")
    else:
        header = "You may add custom in crypto" + file + " file"
        cterm("output", header, "inf")


def cterm(com_type, message, message_type):
    """
        com_type - does it input or output
        message - the text
        message_type - type from iface.json
    """
    begin = cterm.iface["colors"][cterm.iface["pallete"][message_type]]
    marker = cterm.iface["markers"][message_type]
    res_line = "{0}{1}{2}".format(begin, marker, message)
    if com_type == "input":
        res_line += cterm.iface["colors"][cterm.iface["pallete"]["def"]]
        return input(res_line)
    print(res_line)


try:
    cterm.iface = download_json("iface_storage/iface.json")
except FileNotFoundError:
    exit()
