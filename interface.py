def draw_header():
    try:
        with open("crypto.head") as head_im:
            header = head_im.read()
            header = "\033[36m" + header + "\033[0m"
    except FileNotFoundError:
        header = "\033[36mYou may add custom header in crypto.head file\033[0m"
    print(header)


def print_help():
    help_text = """\033[34mCrypto helper:

hack        -> hack some algorithm
caesar      -> encrypt/decrypt using caesar algo
xor         -> encrypt/decrypt using xor algo
exit        -> turn off crypto\033[0m
"""
    print(help_text, end='')
