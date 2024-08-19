def bin_coef_1(n, k):
    return int(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))


# The recursive natural solution
def bin_coef_2(n, k):
    if k == 0 or k == n:
        return 1
    return bin_coef_2(n - 1, k - 1) + bin_coef_2(n - 1, k)


# Solution with dynamic programming (supported by a table)
def bin_coef_3(n, k):
    c = 0
    v = [1] * (k + 1)

    for i in range(n + 1):
        for j in range(k, 0, -1):
            if j < i:
                v[j] = v[j - 1] + v[j]

    return v[k]


def coin_change(N, d):
    n = len(d)
    matrix = [[0] * (N + 1) for i in range(n)]

    for i in range(0, n):
        for j in range(1, N + 1):
            if i == 0 and j < d[i]:
                matrix[i][j] = math.inf
            elif i == 0:
                matrix[i][j] = 1 + matrix[0][j - d[0]]
            elif j < d[i]:
                matrix[i][j] = matrix[i - 1][j]
            else:
                matrix[i][j] = min(matrix[i - 1][j], 1 + matrix[i][j - d[i]])

    return matrix


# Example values
N = 8
d = [1, 4, 6]

# Showing results
dp_table = coin_change(N, d)
pd.DataFrame(dp_table, index=d)


def coins_list(c, d, N, verbose=False):
    coins_list = []
    i = len(d) - 1
    j = N

    while i > -1 and j > -1:
        if verbose:
            print(i, j)

        if i - 1 >= 0 and c[i][j] == c[i - 1][j]:
            i = i - 1
        elif j - d[i] >= 0 and c[i][j] == 1 + c[i][j - d[i]]:
            coins_list.append(d[i])
            j = j - d[i]
        else:
            break

    return coins_list


# List of coins for each scenario
for j in range(0, N + 1):
    print(j, "->", coins_list(dp_table, d, j))


def best_knapsack(w, v, W):
    n = len(v)
    matrix = [[0] * (W + 1) for i in range(n)]

    for i in range(0, n):
        for j in range(1, W + 1):
            if i == 0 and j < w[i]:
                matrix[i][j] = -math.inf
            elif i == 0:
                matrix[i][j] = v[i]
            elif j < w[i]:
                matrix[i][j] = matrix[i - 1][j]
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - w[i]] + v[i])

    return matrix


# Example values
w = [1, 2, 5, 6, 7]
v = [1, 6, 18, 22, 28]
max_weight = 11

# Run algorithm
dp_table = best_knapsack(w, v, max_weight)
df_index = ["w:" + str(w[i]) + ", v:" + str(v[i]) for i in range(len(v))]
pd.DataFrame(dp_table, index=df_index)


def items_list(values, v, w, W, verbose=False):
    item_list = []
    i = len(w) - 1
    j = W

    while i > -1 and j > -1:
        if verbose:
            print(i, j)

        if i - 1 >= 0 and values[i][j] == values[i - 1][j]:
            i = i - 1
        elif (
            i - 1 >= 0
            and j - w[i] >= 0
            and values[i][j] == values[i - 1][j - w[i]] + v[i]
        ):
            item = {"w": w[i], "v": v[i]}
            item_list.append(item)
            j = j - w[i]
            i = i - 1
        elif i == 0 and values[i][j] == v[i]:
            item = {"w": w[i], "v": v[i]}
            item_list.append(item)
            break
        else:
            break

    return item_list


# List of coins for each scenario
for j in range(0, max_weight + 1):
    print(j, "->", items_list(dp_table, v, w, j))


def lcs(a, b):
    n = len(a)
    m = len(b)
    matrix = [[0] * (m + 1) for i in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                matrix[i][j] = 1 + matrix[i - 1][j - 1]
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])

    return matrix


# Example values
a = ["X", "M", "J", "Y", "A", "U", "Z"]
b = ["M", "Z", "J", "A", "W", "X", "U"]

# Run algorithm
dp_table = calc_lcs(a, b)
pd.DataFrame(dp_table, index=["-"] + a, columns=["-"] + b)


def get_lcs(matrix, a, b, verbose=False):
    lc_seq = []
    i = len(a)
    j = len(b)

    while i > -1 and j > -1:
        if verbose:
            print(i, j)

        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            lc_seq.append(a[i - 1])
            i = i - 1
            j = j - 1
        elif j > 0 and (i == 0 or matrix[i][j - 1] >= matrix[i - 1][j]):
            j = j - 1
        elif i > 0 and (j == 0 or matrix[i][j - 1] < matrix[i - 1][j]):
            i = i - 1
        else:
            break

    return list(reversed(lc_seq))


get_lcs(dp_table, a, b)
