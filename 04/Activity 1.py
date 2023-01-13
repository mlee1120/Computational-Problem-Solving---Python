def start():
    m = "ZOO"
    s = "S0,2"
    s2 = s.split(",")
    print(shift_2(m, s2[0][1], s2[1]))


def rotate_1(s):
    return s[-1:] + s[:-1]


def rotate_2(s, n):
    return s[-n:] + s[:-n]


def shift_1(c, k):
    k %= 26
    # ASCII table: A~Z = 65~90
    if ord(c) + k > 90:
        return chr(65 + (ord(c) + k - 91))
    else:
        return chr(ord(c) + k)


def shift_2(message, index, exponent):
    exponent = str(int(exponent) % 26)
    # ASCII table: A~Z = 65~90
    if 65 <= ord(message[int(index)]) <= 90:
        if ord(message[int(index)]) + int(exponent) > 90:
            return message[:int(index)] + chr(65 + ord(message[int(index)]) + int(exponent) - 91) + message[
                                                                                                    int(index) + 1:]
        else:
            return message[:int(index)] + chr(ord(message[int(index)]) + int(exponent)) + message[int(index) + 1:]
    # ASCII table: a~z = 97~122
    elif 97 <= ord(message[int(index)]) <= 122:
        if ord(message[int(index)]) + int(exponent) > 122:
            return message[:int(index)] + chr(97 + ord(message[int(index)]) + int(exponent) - 123) + message[
                                                                                                     int(index) + 1:]
        else:
            return message[:int(index)] + chr(ord(message[int(index)]) + int(exponent)) + message[int(index) + 1:]


if __name__ == "__main__":
    start()