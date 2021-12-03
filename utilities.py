def hex2bin(s):
    ans = (bin(int(s, 16))[2:]).zfill(len(s) * 4)
    return ans


def bin2hex(s):
    ans = hex(int(s, 2)).upper()[2:]
    return ans


def bin2dec(binary):
    return int(str(binary), 2)


def dec2bin(num):
    ans = bin(num)[2:].zfill(4)
    return ans


def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation


def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k