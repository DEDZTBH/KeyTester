import numpy
# import copy
import time

mod = 97

broken_private_key = numpy.loadtxt(fname="broken_private_key.csv", dtype=int, delimiter=",")
encoded = numpy.loadtxt(fname="encoded.csv", dtype=int, delimiter=",")
decoded = numpy.loadtxt(fname="decoded.csv", dtype=int, delimiter=",")
print "broken_private_key\n", broken_private_key
print "\nencoded\n", encoded
print "\ndecoded\n", decoded


class BrokenVal:
    def __init__(self, row, column):
        self.r = row
        self.c = column
        self.val = 0


broken_vals = []
print '\nFound breaks:'

for ri, r in enumerate(broken_private_key):
    for ci, c in enumerate(r):
        if c < 0:
            print str(len(broken_vals)) + ":[" + str(ri) + "][" + str(ci) + "], "
            broken_vals.append(BrokenVal(ri, ci))


def iteration_add(digit):
    if digit >= len(broken_vals):
        return False
    if broken_vals[digit].val >= mod - 1:
        broken_vals[digit].val = 0
        return iteration_add(digit + 1)
    else:
        broken_vals[digit].val += 1
        return True


# success = []
successCnt = 0
depleted = len(broken_vals) == 0
print "\nStart testing & start timer..."
t1 = time.time()
while not depleted:
    # st = []
    for slot, v in enumerate(broken_vals):
        broken_private_key[v.r][v.c] = v.val
        # st.append(str(slot) + ":[" + str(v.r) + "][" + str(v.c) + "] = " + str(v.val) + ", ")
    # print st
    if numpy.array_equal(numpy.mod(numpy.dot(encoded, broken_private_key), mod), decoded):
        # success.append(copy.deepcopy(broken_private_key))
        successCnt += 1
        fname = "solution" + str(successCnt) + '.csv'
        print "Here's a solution! Saved to " + fname
        print broken_private_key
        numpy.savetxt(fname=fname, X=broken_private_key, delimiter=",")
    depleted = not iteration_add(0)
print "DONE! Finished " + str(mod ** len(broken_vals)) + " cycles in " + str(time.time() - t1) + "s"

# print "\nsuccess:\n" + str(success)
