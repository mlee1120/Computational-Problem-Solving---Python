"""
file: transformer.py
description: CSCI 603 hw4 Group4
language: python3
author: Michael Lee ml3406@RIT.EDU
author: Joseph Gawlowicz jg2348@RIT.EDU/joseph.gawlowicz@live.com
"""

import sys

# .../transformer.py message instruction output e/d
if len(sys.argv) != 1:
    if len(sys.argv) != 5:
        print("$ python3 transformer.py message instruction output e/d")
        assert sys.argv[4] != "e" or sys.argv[4] != "d"
    message = sys.argv[1]
    instruction = sys.argv[2]
    output = sys.argv[3]
    e_d = sys.argv[4]


def start():
    """
    Arguments: .../transformer.py message instruction output e/d
    If no arguments are passed to the program, the user will be prompted for this information.
    Calls process_file to deal with the files once the filenames are initialized.
    :param e_d: to determine either to encrypt or decrypt the input message
    """
    global e_d
    try:
        if len(sys.argv) == 1:

            # JAG revisions start here for input
            print("TEXT TRANSFORMER")
            print("This program encrypts or decrypts user text files based on user input.")
            print()
            print("The following inputs are not case sensitive.")
            print("Please enter the input file name with extension (such as plaintext.txt or ciphertext.txt): ")
            filename1 = input()
            print()
            print("Please enter the transformation instructions file name with extension (such as instructions.txt): ")
            filename2 = input()
            print()
            print("Please enter the output filename with extension (such as plaintext.txt or ciphertext.com): ")
            filename3 = input()
            print()
            print("Choose encryption or decryption transformation by entering e or d:")
            e_d = input()

            # JAG revisions end here for input

            if e_d != "e" and e_d != "d":
                print("Please enter e or d.")
                assert e_d == "e" or e_d == "d"
        else:
            filename1 = message
            filename2 = instruction
            filename3 = output
        process_file(filename1, filename2, filename3)
    except FileNotFoundError as fnfe:
        print(fnfe, file=sys.stderr)  # print the error on the standard output


def process_file(fn1, fn2, fn3):
    """
    Reads files and calls shift() to encrypt or decrypt the input message with corresponding instructions.
    Write transformed message into the output file.
    :param fn1: file path name of the input message
    :param fn2: file path name of the transformation instructions
    :param fn3: file path name of the output
    """
    # list that stores input message line by line
    m = []
    # list that stores transportation instructions line by line
    i = []
    # Read and display contents of input file
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Contents of the input file " + fn1 + ":")
    with open(fn1) as f:
        for line in f:
            # strip the newline at the end of the line
            line = line.strip()
            print(line)
            m.append(line)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Read and display the contents of instruction file
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Contents of the instruction file " + fn1 + ":")
    with open(fn2) as f:
        for line in f:
            line = line.strip()
            print(line)
            i.append(line)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Display contents of output file
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Contents of the output file " + fn3 + ":")
    f = open(fn3, 'w')
    for c1 in range(len(m)):
        f.write(shift(m[c1], i[c1]) + "\n")
        print(shift(m[c1], i[c1]))
    # Close the file after finishing writing to prevent leaking resources problems
    f.close()
    print("Output file " + fn3 + " is written.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Program ended successfully.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # End of process_file()


def shift(sentence1, operation1):
    """
    Calls transformer functions according to the first letter from the instructions.
    When encrypting a message, transformation instructions should be applied from left to right.
    When decrypting a message, transformation instructions should be applied from right to left.
    :param sentence1: a line of input message
    :param operation1: the corresponding transformation instruction
    :return: transformed message
    """
    # split operation 1 to a list that stores one or a series of transformation instructions
    operation1 = operation1.split(";")
    for c2 in range(len(operation1)):
        sentence2 = ""
        # encrypt the input message with instructions from left to right
        if e_d == "e":
            if operation1[c2][0] == "S":
                operation2 = operation1[c2].split(",")
                if len(operation2) == 1:
                    operation2.append("1")
                sentence2 += sigma(sentence1, int(operation2[0][1:]), int(operation2[1]))
            elif operation1[c2][0] == "R":
                if len(operation1[c2]) == 1:
                    operation1[c2] += "1"
                sentence2 += rho(sentence1, int(operation1[c2][1:]))
            elif operation1[c2][0] == "D":
                operation2 = operation1[c2].split(",")
                if len(operation2) == 1:
                    operation2.append("1")
                sentence2 += delta(sentence1, int(operation2[0][1:]), int(operation2[1]))
            elif operation1[c2][0] == "T":
                operation2 = operation1[c2].split(",")
                if operation2[0][1] != "(":
                    operation2[0] = operation2[0][:1] + "(" + str(len(sentence1)) + ")" + operation2[0][1:]
                sentence2 += tau(sentence1, int(operation2[0][2:operation2[0].index(")")]),
                                 int(operation2[0][operation2[0].index(")") + 1:]), int(operation2[1]))
            elif operation1[c2][0] == "E":
                if len(operation1[c2]) == 1:
                    operation1[c2] += "1"
                if e_d == "d":
                    sentence2 += encryption(sentence1, -int(operation1[c2][1:]) % 26, len(sentence1) - 1)
                else:
                    sentence2 += encryption(sentence1, int(operation1[c2][1:]) % 26, len(sentence1) - 1)
        # decrypts the encrypted message with instructions from right to left
        else:
            if operation1[len(operation1) - 1 - c2][0] == "S":
                operation2 = operation1[len(operation1) - 1 - c2].split(",")
                if len(operation2) == 1:
                    operation2.append("1")
                sentence2 += sigma(sentence1, int(operation2[0][1:]), int(operation2[1]))
            elif operation1[len(operation1) - 1 - c2][0] == "R":
                if len(operation1[len(operation1) - 1 - c2]) == 1:
                    operation1[len(operation1) - 1 - c2] += "1"
                sentence2 += rho(sentence1, int(operation1[len(operation1) - 1 - c2][1:]))
            elif operation1[len(operation1) - 1 - c2][0] == "D":
                operation2 = operation1[len(operation1) - 1 - c2].split(",")
                if len(operation2) == 1:
                    operation2.append("1")
                sentence2 += delta(sentence1, int(operation2[0][1:]), int(operation2[1]))
            elif operation1[len(operation1) - 1 - c2][0] == "T":
                operation2 = operation1[len(operation1) - 1 - c2].split(",")
                if operation2[0][1] != "(":
                    operation2[0] = operation2[0][:1] + "(" + str(len(sentence1)) + ")" + operation2[0][1:]
                sentence2 += tau(sentence1, int(operation2[0][2:operation2[0].index(")")]),
                                 int(operation2[0][operation2[0].index(")") + 1:]), int(operation2[1]))
            elif operation1[len(operation1) - 1 - c2][0] == "E":
                if len(operation1[len(operation1) - 1 - c2]) == 1:
                    operation1[len(operation1) - 1 - c2] += "1"
                if e_d == "d":
                    sentence2 += encryption(sentence1, -int(operation1[len(operation1) - 1 - c2][1:]) % 26,
                                            len(sentence1) - 1)
                else:
                    sentence2 += encryption(sentence1, int(operation1[len(operation1) - 1 - c2][1:]) % 26,
                                            len(sentence1) - 1)
        sentence1 = sentence2
    return sentence1


def sigma(string, index, exponent):
    """
    Deals with sigma transformation from hw4 (only A~Z)
    :param string: the input message
    :param index: the position of the character to be transformed
    :param exponent: level of transformation
    :return: the transformed message
    """
    assert 0 <= index < len(string)
    if e_d == "d":
        exponent = -exponent
    exponent = exponent % 26
    # ASCII table: A~Z = 65~90
    if 65 <= ord(string[index]) <= 90:
        if ord(string[index]) + exponent > 90:
            return string[:index] + chr(65 + ord(string[index]) + exponent - 91) + string[index + 1:]
        else:
            return string[:index] + chr(ord(string[index]) + exponent) + string[index + 1:]


def rho(string, exponent):
    """
    Deals with rho transformation from hw4
    :param string: the input message
    :param exponent: level of transformation
    :return: the transformed message
    """
    if e_d == "d":
        exponent = -exponent
    return string[-exponent:] + string[:-exponent]


def delta(string, index, exponent):
    """
    Deals with delta transformation from hw4
    :param string: the input message
    :param index: the position of the character to be duplicated
    :param exponent: level of transformation
    :return: the transformed message
    """
    assert 0 <= index < len(string)
    if e_d == "d":
        string = string[:index] + string[index + exponent:]
    else:
        for _ in range(exponent):
            string = string[:index] + string[index] + string[index:]
    return string


def tau(string1, segment, index1, index2):
    """
    Deals with tau transformation from hw4
    :param string1: the input message
    :param segment: the amount of segments string1 to be cut into
    :param index1: the position of segment 1 to be swapped
    :param index2: the position of segment 2 to be swapped
    :return: the transformed message
    """
    # list that stores segments of string1
    string1_cut = []
    string2 = ""
    # cut string1 into segments
    for c3 in range(segment):
        string1_cut.append(string1[c3 * len(string1) // segment:(c3 + 1) * len(string1) // segment])
    assert 0 <= index1 < index2 < len(string1_cut)
    # using tuple to swap
    string1_cut[index1], string1_cut[index2] = string1_cut[index2], string1_cut[index1]
    # concatenate the segments into string2
    for c4 in range(len(string1_cut)):
        string2 += string1_cut[c4]
    return string2


def encryption(string, exponent, index):
    """
    All characters in the input message are converted into ASCII numbers and shifted by an amount 'exponent', and then
    converted back to corresponding characters. For example: AAA to ZZZ, abc to bcd, and so on.
    (Using recursion to accomplish the transformation)
    :param string: the input message
    :param exponent: level of transformation
    :param index: character position
    :return: the transformed message
    """
    if index >= 0:
        # ASCII table: A~Z = 65~90
        if ord(string[index]) + exponent > 90:
            return encryption(string, exponent, index - 1) + chr(65 + ord(string[index]) + exponent - 91)
        else:
            return encryption(string, exponent, index - 1) + chr(ord(string[index]) + exponent)
    else:
        return ""


# main conditional guard
# script execution/run
# the following condition checks whether we are
# running as a script, in which case run the test code.
# if the file is being imported, don't run the test code.
if __name__ == "__main__":
    start()
