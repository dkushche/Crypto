""" Elliptic Math tools

Set of tools for dealing with ellipcit curves cryptology

"""

import copy
from .math_tools import is_prime, inverse_modulo_numb


class elliptic_point:
    """
    point on elliptic curve

    """
    elliptic_curve = {}

    def set_curve(a, b, p):
        if not is_prime(p):
            raise ValueError(f"p = {p} is not prime")
        if p <= 3:
            raise ValueError("p must be bigger then 3")
        if (4 * pow(a, 3) + 27 * pow(b, 2)) % p == 0:
            raise ValueError(f"Incorrect curve {a}, {b}, {p}")

        elliptic_point.elliptic_curve = {
            "a": a,
            "b": b,
            "p": p
        }

    def belong_to_curve(point):
        return (
            (
                point.x ** 3 +
                elliptic_point.elliptic_curve["a"] * point.x +
                elliptic_point.elliptic_curve["b"]
            ) - point.y ** 2
        ) % elliptic_point.elliptic_curve["p"] == 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Elliptic point ({self.x}, {self.y})"

    def __neg__(self):
        return elliptic_point(
            self.x,
            -self.y % elliptic_point.elliptic_curve["p"]
        )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if not isinstance(other, elliptic_point):
            raise ValueError("Can't add elliptic_point to other type")

        if self == elliptic_point(0, 0) or other == elliptic_point(0, 0):
            return copy.deepcopy(
                self if other == elliptic_point(0, 0) else other
            )

        if self == other:
            if self.y != 0:
                m = ((3 * (self.x ** 2) +
                        elliptic_point.elliptic_curve["a"]) *
                        inverse_modulo_numb(
                        2 * self.y, elliptic_point.elliptic_curve["p"]))
            else:
                return elliptic_point(0, 0)
        else:
            if other.x - self.x != 0:
                m = ((other.y - self.y) *
                        inverse_modulo_numb(
                        other.x - self.x,
                        elliptic_point.elliptic_curve["p"]
                        ))
            else:
                return elliptic_point(0, 0)

        m %= elliptic_point.elliptic_curve["p"]

        new_x = ((m ** 2 - self.x - other.x)
                    % elliptic_point.elliptic_curve["p"])
        new_y = ((self.y + m * (new_x - self.x))
                    % elliptic_point.elliptic_curve["p"])
        return elliptic_point(
            new_x, -new_y % elliptic_point.elliptic_curve["p"]
        )


    def __sub__(self, other):
        if isinstance(other, elliptic_point):
            return self.__add__(other.__neg__())
        raise ValueError("Can't sub elliptic_point to other type")

    def __mul__(self, other):
        if isinstance(other, int):
            if other == 0:
                return elliptic_point(0, 0)
            temp = copy.deepcopy(self)
            res = self
            while other > 1:
                res = res + temp
                other -= 1
            return res
        raise ValueError("Can't mult elliptic_point not on int")
