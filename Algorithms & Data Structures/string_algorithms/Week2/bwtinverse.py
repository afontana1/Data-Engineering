# python3
import sys


def map_forward(data, dict_count):
    if data[0] == "$":
        return 0
    elif data[0] == "A":
        return data[1]
    elif data[0] == "C":
        return dict_count[0] + data[1]
    elif data[0] == "G":
        return dict_count[0] + dict_count[1] + data[1]
    elif data[0] == "T":
        return dict_count[0] + dict_count[1] + dict_count[2] + data[1]
    return False


def InverseBWT(bwt):
    # write your code here
    dict_count = [0, 0, 0, 0, 1]
    list_map = []
    for word in bwt:
        if word == "A":
            dict_count[0] += 1
            list_map.append(("A", dict_count[0]))
        elif word == "C":
            dict_count[1] += 1
            list_map.append(("C", dict_count[1]))
        elif word == "G":
            dict_count[2] += 1
            list_map.append(("G", dict_count[2]))
        elif word == "T":
            dict_count[3] += 1
            list_map.append(("T", dict_count[3]))
        else:
            list_map.append(("$", dict_count[4]))

    max_length = len(bwt)
    start = ("$", 1)
    t = [""] * max_length
    for i in range(max_length):
        idx = map_forward(start, dict_count)
        t[max_length - i - 1] = bwt[idx]
        start = list_map[idx]
    return "".join(t[1:]) + "$"


if __name__ == "__main__":
    bwt = sys.stdin.readline().strip()
    #    bwt = 'AC$A'
    #    bwt = 'AGGGAA$'
    #    bwt = 'CCCCCCCCCC$'
    #    bwt = 'CGAA$AGTACATGGAAAAGGAAA'
    print(InverseBWT(bwt))
