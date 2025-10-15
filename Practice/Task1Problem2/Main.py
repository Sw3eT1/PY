import LeastCommonMultiple

while True:
    try:
        first_number = int(input("Enter the first number you want to check: "))
        if first_number > 0:
            break
        else:
            print("Please enter an integer greater than 0.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

while True:
    try:
        second_number = int(input("Enter the second number you want to check: "))
        if second_number > 0:
            break
        else:
            print("Please enter an integer greater than 0.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

print(f"LCM({first_number}, {second_number}) = {LeastCommonMultiple.lest_common_multiple(first_number, second_number)}")
