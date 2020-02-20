def form_frequency_dict(data):
    """
        Forms sorted dictionary with
        probabilities values for every character
    """
    laters = {}

    for char in data:
        if char in laters:
            laters[char] += 1
        else:
            laters.update({char: 1})
    for later in laters:
        laters[later] = laters[later] / len(data) * 100
    items = laters.items()
    laters = {
        k: v for k, v in sorted(items, key=lambda item: item[1], reverse=True)
    }
    return laters


def freq_analys(data, lang, algo, verbose):
    raise ValueError("Freq analysis")
