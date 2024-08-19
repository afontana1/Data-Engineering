import matplotlib.pyplot as plt


# Graph setup

plt.xlabel("iteration")
plt.ylabel("value")
plt.title("Graph")


# Variables

number = 1  # initial positive number
iterations = 0  # to count iteration
List_iteration = [0]  # lists to plot
List_number = [0]


# Interaction
print("\n Do you want to start from a specific number [y/n] ?")
option_number = str(input(" default is 1, enter y or n to continue : "))

if option_number == "Y" or option_number == "y":

    number = int(input(" Enter the number : "))

print("\n Press Ctrl + C any time to interrupt and to see the plotted graph \n")
start = str(input(" Press Enter to begin ! \n"))

num = number


try:  # for KeyboardInterrupt code section/block

    while True:

        if (num % 2) == 0:  # if number is even make it odd
            num = int(num / 2)
            iterations += 1  # increment

            List_number.append(num)  # Add number/value in list, every time
            List_iteration.append(iterations)  # Add iteration value/increment
            plt.plot(
                List_iteration, List_number, "b-o"
            )  # Pass varibles as arguments to plot, with graph style

        else:
            num = int(num * 3 + 1)  # if number is odd make it even
            iterations += 1

            List_number.append(num)  # Add number value in list, every time
            List_iteration.append(iterations)  # iteration
            plt.plot(
                List_iteration, List_number, "b-o"
            )  # Pass varibles as arguments to plot, with graph style

        if num == 1:  # Next number !
            print(" Number : ", number, ", Iterations : ", iterations, ", True ", "\n")
            number += 1  # increment
            iterations = 0
            num = number

            List_iteration = [0]  # reset/empty lists for next round
            List_number = [0]

        elif num == 0:  # conjecture break , alert !
            print(" Number : ", number, ", False ", "\n")
            break  # exit loop


except KeyboardInterrupt:  # if KeyboardInterrupt occur (Ctrl+C by user end programme)
    print(
        3 * "\n",
        " Keyboard Interrupt is caught !",
        2 * "\n",
        " Please wait, showing graph.....",
        2 * "\n",
    )
    plt.show()  # show ploted graph
    print("\n", " exit", 4 * "\n")
