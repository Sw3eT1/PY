import math

def lest_common_multiple(number_1, number_2):
    factors_1 = prime_factorization(number_1)
    factors_2 = prime_factorization(number_2)

    distinct_list_of_all_primes = set(list(factors_1.keys()) + list(factors_2.keys()))

    lcm = 1

    for i in distinct_list_of_all_primes:
        exponetial = max(factors_1.get(i, 0), factors_2.get(i, 0))
        lcm *= i ** exponetial
    return lcm


def prime_factorization(number):
    factors = dict()

    if number % 2 == 0:
        factors[2] = 0
    while number % 2 == 0:
        factors[2] += 1
        number //= 2

    counter = 3
    while counter <= math.isqrt(number):
        while number % counter == 0:
            if counter not in factors:
                factors[counter] = 0
            factors[counter] += 1
            number //= counter
        counter += 2

    if number > 1:
        factors[number] = 1

    return factors
