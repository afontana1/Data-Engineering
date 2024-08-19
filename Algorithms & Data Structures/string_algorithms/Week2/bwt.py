# python3
import sys


def BWT(text):
    n = len(text)
    l = list()
    rtext = ""
    for i in range(n):
        l.append(text[i:n] + text[0:i])
    l.sort()
    for word in l:
        rtext += word[n - 1]
    return rtext


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    #    text = 'AA$'
    #    text = 'ACACACAC$'
    #    text = 'AGACATA$'
    #    text = 'AACGATAGCGGTAGA$'
    #    text = 'CC$'
    #    text = 'CCCCCCCCCC$'
    text = "AAGACAGATATAGAAAAAGGGC$"
    print(BWT(text))
