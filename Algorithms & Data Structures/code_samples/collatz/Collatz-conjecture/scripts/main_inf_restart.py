# Variables

number = 1  # initial positive number
iterations = 0  # to count iteration
List_iteration = [0]  # lists to plot
List_number = [0]
## main_num.txt is a file of all numbers (num) encountered during loops, this allows to skip ahead if a loop reaches a previously terminating string.
## main_seq.txt contains all numbers with iterations larger than 0, i.e. numbers who haven't already been encountered previously.

# Interaction
print("\n Do you want to start from a specific number [y/n] ?")
option_number = str(input(" default is 1, enter y or n to continue : "))

if option_number == ["Y", "y"]:
    number = int(input(" Enter the number : "))
try:
    import os

    with open("main_seq.txt", "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline().decode()
        placeKeeper = last_line.find(" ")
        number = last_line[0:placeKeeper]
        number = int(number) + 1
    print(f"We'll be continuing with {number}!")
except Exception:
    print("We'll be starting with 1!")
    number = 1


print("\n Press Ctrl + C any time to quit \n")
start = str(input(" Press Enter to begin ! \n"))

num = number


while True:
    f = open("main_num.txt", "r+")  # Opens ClltzSet.txt for reading
    fileSet = f.read().splitlines()

    if str(num) in fileSet:
        if iterations != 0:
            f.close()  # Closes main_num.txt
            print(
                " Number : ", number, ", Iterations : ", iterations, ", True ", "\n"
            )  # Adds the number, iterations, and sequence to the file if the iterations are not 0.
            f = open("main_seq.txt", "a")
            f.write(f"{number} : {iterations} {List_number}\n")
            f.close()
        number += 1  # increment
        iterations = 0
        num = number

        List_iteration = [0]  # reset/empty lists for next round
        List_number = [0]

    elif (num % 2) == 0:  # if number is even make it odd
        f.write(f"{num}\n")  # Writes the variable to the set
        num = int(num / 2)
        iterations += 1  # increment

        List_number.append(num)  # Add number/value in list, every time
        List_iteration.append(iterations)  # Add iteration value/increment

    else:
        f.write(f"{num}\n")  # Writes the variable to the set
        num = int(num * 3 + 1)  # if number is odd make it even
        iterations += 1

        List_number.append(num)  # Add number value in list, every time
        List_iteration.append(iterations)  # iteration

    if num == 1:  # Next number !
        f.close()  # Closes the file

        f = open("main_seq.txt", "a")
        f.write(f"{number} : {iterations} {List_number}\n")
        f.close()

        print(" Number : ", number, ", Iterations : ", iterations, ", True ", "\n")
        number += 1  # increment
        iterations = 0
        num = number

        List_iteration = [0]  # reset/empty lists for next round
        List_number = [0]

    elif num == 0:  # conjecture break , alert !
        print(" Number : ", number, ", False ", "\n")
        break  # exit loop
