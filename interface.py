def render_static(file):
    try:
        with open("crypto." + file) as head_im:
            header = head_im.read()
            header = "\033[36m" + header + "\033[0m"
    except FileNotFoundError:
        header = "\033[36mYou may add custom in crypto" + file + " file\033[0m"
    print(header)
