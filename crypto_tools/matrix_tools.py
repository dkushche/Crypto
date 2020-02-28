def is_square(mtx):
    """
        Check is matrix square
    """
    for line in mtx:
        if len(line) != len(mtx):
            return False
    return True


def mtx_mult(fmtx, smtx):
    res = [[0 for i in range(len(smtx[0]))] for j in range(len(fmtx))]

    for i in range(len(fmtx)):
        for j in range(len(smtx[0])):
            for k in range(len(smtx)):
                res[i][j] += fmtx[i][k] * smtx[k][j]
    return res


def transpose(mtx):
    return [[mtx[j][i] for j in range(len(mtx))] for i in range(len(mtx[0]))]


def get_minor_mtx(mtx, line, raw):
    res = [[0 for i in range(len(mtx) - 1)] for j in range(len(mtx) - 1)]
    next_inx = 0

    for j in range(0, len(mtx)):
        if j == line:
            continue
        for i in range(0, len(mtx)):
            if i == raw:
                continue
            y = next_inx // (len(mtx) - 1)
            x = next_inx % (len(mtx) - 1)
            res[y][x] = mtx[j][i]
            next_inx += 1
    return res



def EGCD(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = EGCD(b_mod_a, a)
        return (g, y - b_div_a * x, x)



def inverse_modulo_numb(determ, modulo):
    gcd, alpha, beta = EGCD(determ, modulo)
    if abs(gcd) != 1:
        raise ValueError("Values aren't coprime integers gcd {0}".format(gcd))
    return alpha


def inverse_mtx(mtx, by_modulo, modulo = 0):
    determ = det(mtx)
    if determ == 0:
        raise ValueError("Determinant == 0")
    if by_modulo == True:
        inverse_det = inverse_modulo_numb(determ, modulo)
    else:
        inverse_det = 1 / determ
    num_mtx = [[0 if i != j else inverse_det for i in range(len(mtx))] for j in range(len(mtx))]
    if len(mtx) > 2:
        augmented = [[(-1) ** (i + j) * det(get_minor_mtx(mtx, i, j)) for j in range(len(mtx[0]))] for i in range(len(mtx))]
    elif len(mtx) == 2:
        augmented = [[mtx[1][1], -1 * mtx[1][0]], [-1 * mtx[0][1], mtx[0][0]]]
    else:
        raise ValueError("To smole matrix for inversion")
    augmented = transpose(augmented)
    res = mtx_mult(num_mtx, augmented)
    return res


def det(mtx):
    """
        Determinant for matrixes NxN
    """
    if not is_square(mtx):
        raise ValueError("Matrix should be square")
    if len(mtx) == 2:
        return mtx[0][0] * mtx[1][1] - mtx[0][1] * mtx[1][0]
    else:
        result = 0
        sign = 1
        for inx in range(len(mtx)):
            next_mtx = get_minor_mtx(mtx, 0, inx)
            result += sign * (mtx[0][inx] * det(next_mtx))
            sign *= -1
        return result
