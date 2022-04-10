""" Interface

Tools for interacting with CLI from module

"""

import sys
import platform
from time import sleep
from threading import Thread

from .file_manager import download_json, download_text
from .general_tools import utf_decoder


def form_result_from_cp(control_package, frame):
    objs_amount = len(control_package["objs_for_anim"]) + \
                  len(control_package["dynamic_values"])
    result_list = [None for i in range(objs_amount)]
    for anim_obj in control_package["objs_for_anim"]:
        result_list[anim_obj[1]] = anim_obj[0][frame % len(anim_obj[0])]
    for dyn_val in control_package["dynamic_values"]:
        result_list[dyn_val[1]] = dyn_val[0]
    return result_list


def animator(control_package):
    frame = 0
    biggest_anim = max([len(obj[0]) for obj in
                        control_package["objs_for_anim"]])
    while not control_package["stop"]:
        result_list = form_result_from_cp(control_package, frame)
        res = control_package["msg"].format(*result_list)
        cterm("animation", res, "inf")
        frame = (frame + 1) % biggest_anim
        sleep(1 / control_package["fps"])


def create_animation(control_package):
    """
        "control_package" : {
            "msg" : special format string,
            "objs_for_anim" : [
                [anim_list, pos], ...
            ],
            "dynamic_values" : [
                [value, pos], ...
            ],
            "fps": value of fps
        }
    """
    control_package["stop"] = False
    anim_id = Thread(target=animator, args=(control_package, ))
    anim_id.start()
    return anim_id


def destroy_animation(anim_id, control_package):
    control_package["stop"] = True
    anim_id.join()
    cterm("output", "", "inf")


def render_static(file):
    header = download_text(file)
    if header:
        cterm("output", utf_decoder(header), "inf")
    else:
        header = "**** No header ****"
        cterm("output", header, "inf")


def cterm(com_type, message, message_type):
    """
        com_type - does it input or output or animation
        message - the text
        message_type - type from iface.json
    """
    begin = iface_init.iface["colors"][iface_init.iface["pallete"][message_type]]
    marker = iface_init.iface["markers"][message_type]
    res_line = f"{begin}{marker}{message}"
    if com_type == "input":
        res_line += iface_init.iface["colors"][iface_init.iface["pallete"]["def"]]
        return input(res_line)
    if com_type == "animation":
        print("\r" + res_line, end="")
    else:
        print(res_line)

    return res_line


def iface_init(profile_dir):
    try:
        iface_init.iface = download_json(profile_dir + "iface.json")

        if platform.system() == 'Windows':
            for color in iface_init.iface["colors"]:
                iface_init.iface["colors"][color] = ""

        render_static(profile_dir + "crypto.header")
    except FileNotFoundError:
        sys.exit()


iface_init.iface = None # Make in better
