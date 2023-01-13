"""
CSCI-603: Sorting
Author: Searching&Sorting Lecture Slides Page 28
Instructor: Professor Maria Cepeda

Implementations of mergeSort.
"""


def msort(data):
    if (len(data) == 1):
        return data
    midindex = len(data) // 2
    first = msort(data[0:midindex])
    second = msort(data[midindex:len(data)])
    # zip 'em up
    ans = []
    firstind = 0
    secondind = 0
    while firstind < len(first) and secondind < len(second):
        # sorted by the laser score
        if int(first[firstind][first[firstind].index(" ") + 1:]) < int(
                second[secondind][second[secondind].index(" ") + 1:]):
            ans.append(first[firstind])
            firstind += 1
        else:
            ans.append(second[secondind])
            secondind += 1
    # one array is used up
    if firstind < len(first):
        ans.extend(first[firstind:])
    else:
        ans.extend(second[secondind:])
    return ans
