# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
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

keyDist = {}
#text2 = open('key_dist.txt')
WORDS2 = re.findall("\S+",(open('key_dist.txt').read()).lower())
for i in range(2,len(WORDS2),3):
        if(float(WORDS2[i])!=0.0):
            keyDist[(WORDS2[i-2],WORDS2[i-1])] = 1.0/float(WORDS2[i])

#print(keyDist.values())

def findRepProb(a,b):
    sum =0.0
    for c,d in keyDist:
        if(c==a):
            sum += keyDist[(c,d)]
    return 25*0.269*(keyDist[(a,b)]/sum)

print(findRepProb('r','t'))
print(findRepProb('a','d'))
print(findRepProb('b','a'))

def InsertInDict(dict, word, prob):
    if word in dict:
        dict[word] = max(prob, dict[word])
    else:
        dict[word] = prob

def correction(word):
    if(word in WORDS):
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
                if(R[0]==c):
                    continue
                w = L + c + R[1:]
                InsertInDict(dict, w,findRepProb(R[0],c))

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
                    if (R[0] == c):
                        continue
                    w = L + c + R[1:]
                    InsertInDict(fdict, w, findRepProb(R[0],c)*dict[word])

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
            print('wrong: ',file1[i], file2[i])

    print("Accruracy is ", correct*100/total)

compute_accuracy('testdata1.txt', 'correctdata1.txt')
