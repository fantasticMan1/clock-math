"""
Created to compute all the meaningful mathematical arrangements of a sequence
of integers.  Specifically, this script is made to find the percentage of such
meaningful arrangements in 12- and 24-hour time formats.

E.g. 6:51 : 6 - 5 = 1
"""

import sys


class Mode:
    twelve_hour = 0
    twentyfour_hour = 1
    decimal = 2


MODE = Mode.twelve_hour


def add(a, b):
    if a is None or b is None:
        return None

    return a + b


def sub(a, b):
    if a is None or b is None:
        return None

    return a - b


def mul(a, b):
    if a is None or b is None:
        return None

    return a * b


def div(a, b):
    if a is None or b is None:
        return None
    if b == 0:
        return None

    return a / b


def pow_(a, b):
    if a is None or b is None:
        return None
    if a == 0 and b <= 0:
        return None
    if b > 1000:
        return None
    
    return pow(a, b)


def root(a, b):
    if a is None or b is None:
        return None
    if a == 0:
        return None

    return pow_(b, 1/a)


def concat(a, b):
    if a is None or b is None:
        return None
    return a * 10 + b


ops = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
    '^': pow_,
    '√': root,
    '': concat,
}


hits = 0
misses = 0


def test(k, l, m, n, s=sys.stdout):
    global hits, misses, MODE

    if MODE == Mode.twelve_hour:
        s.write(f'{k}{l}:{m}{n} : ')
    else:
        s.write(f'{k}{l}{m}{n}: ')

    for symbol1, op1 in ops.items():
        for symbol2, op2 in ops.items():
            if op1(k, l) == op2(m, n):  # kl = mn
                s.write(f'{k}{symbol1}{l} = {m}{symbol2}{n}\n')
                hits += 1
                return
            if op1(k, op2(l, m)) == n:  # k(lm) = n
                s.write(f'{k}{symbol1}({l}{symbol2}{m}) = {n}\n')
                hits += 1
                return
            if op2(op1(k, l), m) == n:  # (kl)m = n
                s.write(f'({k}{symbol1}{l}){symbol2}{m} = {n}\n')
                hits += 1
                return
            if k == op1(l, op2(m, n)):  # k = l(mn)
                s.write(f'{k} = {l}{symbol1}({m}{symbol2}{n})\n')
                hits += 1
                return
            if k == op2(op1(l, m), n):  # k = (lm)n
                s.write(f'{k} = ({l}{symbol1}{m}){symbol2}{n}\n')
                hits += 1
                return

    s.write(f'-\n')
    misses += 1


if __name__ == '__main__':
    with open('results.txt', 'w') as f:
        for k in range(10):
            for l in range(10):
                if MODE == Mode.twelve_hour and (concat(k, l) > 12 or concat(k, l) <= 0):
                    continue
                elif MODE == Mode.twentyfour_hour and (concat(k, l) > 12 or concat(k, l) < 0):
                    continue

                for m in range(10):
                    for n in range(10):
                        if (MODE == Mode.twelve_hour or MODE == Mode.twentyfour_hour) and concat(m, n) > 59:
                            continue

                        test(k, l, m, n, f)
        f.write(f'\nhits: {hits}, misses: {misses}, hit percentage: {hits/(hits+misses)*100:.2f}%.\n')
