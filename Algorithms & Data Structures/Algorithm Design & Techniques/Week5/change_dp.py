# Uses python3
import sys

# Input Format. Integer money.
# Output Format. The minimum number of coins with denominations 1, 3, 4 that changes money.


def get_change(money):
    coins = [1, 3, 4]  # Denominations of coins
    MinNumCoins = []
    MinNumCoins.append(0)  # If money == 0, we don't need coins

    for m in range(money):  # m from 0 to money - 1
        MinNumCoins.append(
            money + 1
        )  # Initialize the value with money + 1 because the maximum number of coins (regardless of denominations) to change money cannot be greater than changing (money + 1) coins denominated with 1
        for i in range(len(coins)):  # Consider every possible denominations
            if (
                m + 1 >= coins[i]
            ):  # If current amount > denomination, we can change with the coins of that denomination
                NumCoins = (
                    MinNumCoins[m + 1 - coins[i]] + 1
                )  # The number of coins needed is MinNumCoins[money - coins[i]] + 1
                if NumCoins < MinNumCoins[m + 1]:
                    MinNumCoins[m + 1] = NumCoins  # Update the minimal number of coins
    return MinNumCoins[money]


if __name__ == "__main__":
    m = int(sys.stdin.read())
    print(get_change(m))
