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
hill        ->      encrypt/decrypt using hill algo

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

Cryptanalysis:
brute_force ->      hack using brute force(finds address)
freq_analys ->      hack using frequency analysis(gives freq_char of text)

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

help        ->      show this message
exit        ->      turn off crypto

*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\033[0m
"""
    print(help_text, end='')
