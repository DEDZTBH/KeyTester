import numpy
import time

mod = 97

broken_private_key = numpy.loadtxt(fname="broken_private_key.csv", dtype=int, delimiter=",")
broken_private_key_2 = numpy.loadtxt(fname="broken_private_key_2.csv", dtype=int, delimiter=",")
encoded = numpy.loadtxt(fname="encoded.csv", dtype=int, delimiter=",")
decoded = numpy.loadtxt(fname="decoded.csv", dtype=int, delimiter=",")
print "broken_private_key\n", broken_private_key
print "\nencoded\n", encoded
print "\ndecoded\n", decoded


class BrokenVal:
    def __init__(self, row, column, val=0):
        self.r = row
        self.c = column
        self.val = val


broken_vals = []
print '\nFound breaks in PK 1:'
for ri, r in enumerate(broken_private_key):
    for ci, c in enumerate(r):
        if c < 0:
            print str(len(broken_vals)) + ":[" + str(ri) + "][" + str(ci) + "], "
            broken_vals.append(BrokenVal(ri, ci))

broken_vals_2 = []
print '\nFound breaks in PK 2:'
for ri, r in enumerate(broken_private_key_2):
    for ci, c in enumerate(r):
        if c < 0:
            print str(len(broken_vals_2)) + ":[" + str(ri) + "][" + str(ci) + "], "
            broken_vals_2.append(BrokenVal(ri, ci))

validation_vals = []
print '\nFound Validators in decoded:'
for ri, r in enumerate(decoded):
    for ci, c in enumerate(r):
        if c >= 0:
            validation_vals.append(BrokenVal(ri, ci, c))
            lastI = len(validation_vals) - 1
            print str(lastI) + ":[" + str(ri) + "][" + str(ci) + "] = " + str(validation_vals[lastI].val) + ", "


def iteration_add_2(digit):
    if digit >= len(broken_vals_2):
        return False
    if broken_vals_2[digit].val >= mod - 1:
        broken_vals_2[digit].val = 0
        return iteration_add_2(digit + 1)
    else:
        broken_vals_2[digit].val += 1
        return True


def iteration_add(digit):
    if digit >= len(broken_vals):
        return iteration_add_2(0)
    if broken_vals[digit].val >= mod - 1:
        broken_vals[digit].val = 0
        return iteration_add(digit + 1)
    else:
        broken_vals[digit].val += 1
        return True


def validate(matrix):
    flag = True
    for i, val in enumerate(validation_vals):
        if matrix[val.r][val.c] != val.val:
            # if i > 2:
                # print(matrix)
            flag = False
            break
    return flag


successCnt = 0
depleted = len(broken_vals) == 0 and len(broken_vals_2) == 0
print "\nStart testing & start timer..."
t1 = time.time()
while not depleted:
    for v in broken_vals:
        broken_private_key[v.r][v.c] = v.val
    for v in broken_vals_2:
        broken_private_key_2[v.r][v.c] = v.val
    attempt = numpy.mod(
        numpy.dot(
            numpy.dot(encoded, broken_private_key),
            broken_private_key_2),
        mod)
    # if attempt[0][0] == 26 \
    #         and attempt[1][4] == 14 \
    #         and attempt[2][1] == 17 \
    #         and attempt[4][0] == 92 \
    #         and attempt[4][4] == 28:
    #     print(attempt)
    if validate(attempt):
        successCnt += 1
        fname = "solution" + str(successCnt) + '.csv'
        print "Here's a solution! Saved to " + fname
        print attempt
        numpy.savetxt(fname=fname, X=attempt, delimiter=",")

    depleted = not iteration_add(0)
print "DONE! Finished " + str(mod ** len(broken_vals)) + " cycles in " + str(time.time() - t1) + "s"
