__author__ = 'scmason'


def _eq(a, b):
    return a == b


def _gt(a, b):
    return a > b


def _gte(a, b):
    return a >= b


def _lt(a, b):
    return a < b


def _lte(a, b):
    return a <= b


def _ne(a, b):
    return a != b


def _in(a, b):
    return a in b


def _nin(a, b):
    return a not in b


class Keys:
    id = "_id"
    _and = "$and"
    _not = "$not"
    _or = "$or"
    _nor = "$nor"

    comparisons = {
        "$eq": _eq,
        "$gt": _gt,
        "$gte": _gte,
        "$lt": _lt,
        "$lte": _lte,
        "$ne": _ne,
        "$in": _in,
        "$nin": _nin
    }
