# python3
import sys

# Problem. You are going to travel to another city that is located d miles away from your home city. Your car can travel
# at most m miles on a full tank and you start with a full tank. Along your way, there are gas stations at
# distances stop[1], stop[2], . . . , stop[n] from your home city. What is the minimum number of refills needed?
# Input Format. The first line contains an integer d. The second line contains an integer m. The third line
# specifies an integer n. Finally, the last line contains integers stop[1], stop[2], . . . , stop[n].
# Output Format. Assuming that the distance between the cities is d miles, a car can travel at most m miles
# on a full tank, and there are gas stations at distances stop[1], stop[2], . . . , stop[n] along the way, output the
# minimum number of refills needed. Assume that the car starts with a full tank. If it is not possible to
# reach the destination, output −1.
# Note: 0 < stop[1] < stop[2] < ... < stop[n] < d


def compute_min_refills(distance, tank, stops):
    # Greedy algorithm: Go to the farthest station to refill tank.
    # Suppose we have an optimal route R which refills at stop[1] and stop [2]. Consider a subproblem with stop[1], stop[r], stop[2] in which stop[r] is the farthest reachable
    # Suppose stop[1] < stop[r] < stop[2]. Refill at stop[r] instead of stop [2] is also an optimal solution.
    # Otherwise if stop[1] < stop[2] < stop[r]. Refill at stop[r] is optimal because only 1 refill is needed and contradicts that R is an optimal route.
    # Hence, refill at the farthest stop is optimal to the subproblem. Hence, it's a safe move

    n = len(stops)  # Number of stops in the path
    stops.append(distance)  # Add distance to destination to the end of list
    stops = [0] + stops  # Add starting point to the front of list
    num_refills, current_refill = (
        0,
        0,
    )  # Initially, number of refills is 0; current refill status is 0

    while (
        current_refill <= n
    ):  # When current_refill <= n, we haven't arrived the destination
        last_refill = current_refill  # last refill status
        while current_refill <= n and (
            stops[current_refill + 1] - stops[last_refill] <= tank
        ):
            current_refill += 1  # Proceed to next stop until 1) destination or 2) insufficient fuel for traveling from stops[last_refill] to stops[current_refill + 1]
        if (
            current_refill == last_refill
        ):  # This occurs if the above while loop is not executed i.e. cannot reach destination with full tank
            return -1
        if (
            current_refill <= n
        ):  # After the above while loop is finished, the farthest stop is reached for refilling, so the number of refills + 1
            num_refills += 1

    return num_refills


if __name__ == "__main__":
    d, m, _, *stops = map(int, sys.stdin.read().split())
    print(compute_min_refills(d, m, stops))
