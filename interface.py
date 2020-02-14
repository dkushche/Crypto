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
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

Cryptography:
caesar      ->      encrypt/decrypt using caesar algo
xor         ->      encrypt/decrypt using xor algo
playfair    ->      encrypt/decrypt using playfair algo

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

Cryptanalysis:
brute_force ->      hack using brute force
freq_analys ->      hack using frequency analysis

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

help        ->      show this message
exit        ->      turn off crypto\033[0m

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
"""
    print(help_text, end='')
