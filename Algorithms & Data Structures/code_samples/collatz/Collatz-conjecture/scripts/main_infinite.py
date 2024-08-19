# Variables

number = 1  # initial positive number
iterations = 0  # to count iteration in while loop


# Interaction
print("\n Do you want to start from a specific number [y/n] ?")
option_number = str(input(" default is 1, enter y or n to continue : "))

if option_number == "Y" or option_number == "y":

    number = int(input(" Enter the number : "))

print("\n Press Ctrl + C any time to quit \n")
start = str(input(" Press Enter to begin ! \n"))

num = number

while True:

    if (num % 2) == 0:  # if number is even make it odd
        num = int(num / 2)
        iterations += 1

    else:
        num = int(num * 3 + 1)  # if number is odd make it even
        iterations += 1

    if num == 1:
        print(" Number : ", number, ", Iterations : ", iterations, ", True ", "\n")
        number += 1
        iterations = 0
        num = number

    elif num == 0:  # conjecture break , alert!
        print(" Number : ", number, ", False ", "\n")
        end = str(
            input(" Press Enter to close \n")
        )  # wait for input, prevent from auto close.
        break  # exit loop
