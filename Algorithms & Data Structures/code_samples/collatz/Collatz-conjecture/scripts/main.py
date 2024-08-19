import matplotlib.pyplot as plt

# Graph setup

plt.xlabel("iteration")
plt.ylabel("value")
plt.title("Graph")

# Interaction

print("\n")
number = int(input(" Pick a number & Press enter 1 2 3 4 5 6 7 8 9... >>> "))
print("\n")

print("  ", number, " Good choise \n")

print(
    """ Now we are going to apply two rules \n
 If the number is odd, we multiply by three and add one [ x3+1 ] \n
 If the number is even, we divide by two [ /2 ]
\n"""
)
print(" Now we keep applying these two rules \n")

start = str(input("    Press Enter to begin ! \n"))

# Variables

iterations = int(0)  # to count iteration in while loop
List_iteration = [0]  # empty list for  iterations ; list to plot
List_number = [0]  # empty list for  iterations ; list to plot

# infinity loop

while True:

    if (number % 2) == 0:  # modulo operator to get the remainder

        number = int(number / 2)  # if number is even make it odd
        print("          ", number)

        iterations = iterations + 1  # Increment

        List_number.append(number)  # Add number/value in list, every time
        List_iteration.append(
            iterations
        )  # Add iteration value/increment in list, every time
        plt.plot(
            List_iteration, List_number, "b-o"
        )  # Pass varibles as arguments to plot, with graph style

        plt.pause(0.0001)  # pause for interval seconds
        # graph figure, will be updated and displayed before the pause (show data ploting live/animation)

    else:
        number = int(number * 3 + 1)  # if number is odd make it even
        print("          ", number)

        iterations = iterations + 1  # Increments

        List_number.append(number)  # Add number/value in list, every time
        List_iteration.append(
            iterations
        )  # Add iteration value/increment in list, every time
        plt.plot(
            List_iteration, List_number, "b-o"
        )  # Pass varibles as arguments to plot, with graph style

        plt.pause(0.0001)  # pause for interval seconds
        # graph figure, will be updated and displayed before the pause (show data ploting live/animation)

    if number == 1:  # Stop !!
        print("\n")
        print(
            " We are in the loop, and the lowest number is one. Every positive integer, if you apply these rules,"
        )
        print(
            " will eventually end up in the 4, 2, 1 loop. Commonly called Collatz conjecture or 3N+1."
        )
        print(
            " And the number you get by applying 3x+1 are called hailstone numbers \n"
        )
        print(" Iterations: ", iterations, "\n")
        plt.show()  # show ploted graph
