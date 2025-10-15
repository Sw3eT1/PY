import SieveOfEratosthenes

while True:
    try:
        upper_limit = int(input("Enter the upper limit of range you want to check: "))
        if upper_limit > 2:
            break
        else:
            print("Please enter an integer greater than 2.")
    except ValueError:
        print("Invalid input. Please enter an integer.")


print(SieveOfEratosthenes.prime_numbers_with_sieve(upper_limit))