def prime_numbers_with_sieve(upper_limit):
    if upper_limit < 2:
        return []

    is_eliminated = [False] * (upper_limit + 1)
    is_eliminated[0] = is_eliminated[1] = True

    p = 2
    while p * p <= upper_limit:
        if not is_eliminated[p]:
            for m in range(p * p, upper_limit + 1, p):
                is_eliminated[m] = True
        p += 1

    primes = [i for i in range(2, upper_limit + 1) if not is_eliminated[i]]
    return primes
