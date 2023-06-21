import re
from collections import Counter
import time

# All words in the corpus text
def words(text): return re.findall(r'\w+', text.lower())

# store frequency of each word in a hash-map
WORDS = Counter(words(open('big.txt').read()))

print(len(WORDS))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def InsertInDict(dict, word, prob):
    if word in dict:
        dict[word] = max(prob, dict[word])
    else:
        dict[word] = prob

def correction(word):
    if word in WORDS:
        return word
# edit 1
    letters = 'abcdefghijklmnopqrstuvwxyz'
    dict = {}
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    # delete logic
    for L, R in splits:
        if R:
            w = L + R[1:]
            InsertInDict(dict, w, .203)

    # transpose logic
    for L, R in splits:
        if len(R) > 1:
            w = L + R[1] + R[0] + R[2:]
            InsertInDict(dict, w, .131)

    # replaces
    for L,R in splits:
        if R:
            for c in letters:
                w = L + c + R[1:]
                InsertInDict(dict, w, .269)

    # inserts
    for L, R in splits:
        for c in letters:
            w = L + c + R
            InsertInDict(dict, w, .344)

    # print(dict)

    ans = ''
    prob = 0.0
    for w in dict:
        if dict[w] * P(w) > prob:
            ans = w
            prob = dict[w] * P(w)
    if(ans != ''):
        return ans
    # edits2
    fdict = {}
    for word in dict:
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        # delete logic
        for L, R in splits:
            if R:
                w = L + R[1:]
                InsertInDict(fdict, w, .203*dict[word])

        # transpose logic
        for L, R in splits:
            if len(R) > 1:
                w = L + R[1] + R[0] + R[2:]
                InsertInDict(fdict, w, .131*dict[word])

        # replaces
        for L, R in splits:
            if R:
                for c in letters:
                    w = L + c + R[1:]
                    InsertInDict(fdict, w, .269*dict[word])

        # inserts
        for L, R in splits:
            for c in letters:
                w = L + c + R
                InsertInDict(fdict, w, .344*dict[word])

    ans = ''
    prob = 0.0
    for w in fdict:
        if fdict[w]*P(w) > prob:
            ans = w
            prob = fdict[w]*P(w)

    return ans or word

# w = correction('hehp')
# p1 = P('hey')
# p2 = P('help')
# print(p1/p2)
# print(w)

w = correction('lpck')
print(w)

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    start = time.perf_counter()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.perf_counter() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))


def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

def compute_accuracy(testfile, correctfile, verbose = False):
    start = time.perf_counter()
    good, unknown = 0, 0
    file1 = []
    file2 = []
    # opening the text file
    with open(testfile, 'r') as file:
        for line in file:
            for word in line.split():
                file1.append(correction(word.lower()))

    with open(correctfile, 'r') as file:
        for line in file:
            for word in line.split():
                file2.append(word.lower())

    correct = 0
    total = max(len(file1), len(file2))

    for i in range(1, min(len(file1), len(file2))):
        if file1[i] == file2[i]:
            correct = correct + 1
        else:
            print(file1[i], file2[i])

    print("Accruracy is ", correct*100/total)

#spelltest(Testset(open('spell-testset1.txt'))) # Development set
#spelltest(Testset(open('spell-testset2.txt'))) # Final test set
#spelltest(Testset(open('aspell.txt'))) # Development set
compute_accuracy('testdata.txt', 'correctdata.txt')