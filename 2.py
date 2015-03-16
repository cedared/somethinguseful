

def sloop(j):
    i = 0
    numbers = []

    while i < int(j):
        print "At the top i is %d." % i
        numbers.append(i)
        i += 1
        print "Numbers now: ", numbers
        print "At the bottom is %d." % i
        print j

    print "Numbers is:"

    for num in numbers:
        print num


# print"Please input a number that is more-than-equal 1."
input_num = raw_input("Please input a number that is more-than-equal 1>>>")

sloop(input_num)