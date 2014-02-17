#! /usr/bin/python

# e-satis @ stackoverflow: http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained

# Iteration : Going over items in a list, one-by-one

myList=[1,2,3]
for i in myList: # "for X in Y" is an iteration pattern
    print i,
print

# The retrieval of the next item using the iterator is done by calling its next() method.

#==========
print

# Iterables
# In the example above, 'myList' is an iterable object, because it comprises items which can be iterated over.

myList2= [ x*x for x in range(3)] # creating a list using list comprehension
for i in myList2: # every Y you can use "for X in Y" on is an iterable: Arrays (lists/tuples/dictionaries/strings), files, ... (this independence of variable type is called duck typing: "If it walks like a duck...")
    print i,
print

# Iterating over an iterable is repeatable and non-destructive of the iterable.
# The iterable objects become very large if all possible values need to be stored in memory in advance.

#=====================================================================
print

# Generators: Iterators which generate the iteration values on-the-fly
# i.e. the values are not all stored in memory in advance,
# but can only be iterated over once.

myGenerator=(x*x for x in range(3))
print myGenerator # 'myGenerator' is an initerable 'generator object'
for i in myGenerator:
    print i,
print

# Once this 'for' loop reaches its end, you can't 'for i in myGenerator' again...
# 'myGenerator' evaluates inside the loop, not before it (lazy evaluation)
# this improves performace, especially for large lists.

print "Timing. This may take a few seconds..."
import timeit
print timeit.timeit('sum(xrange(200))',setup='') # uses generator
print timeit.timeit('sum(range(200))',setup='') # does not use generator


#=============================================================================
print

# Yield: a keyword used like 'return', in a function which returns a generator
# c.f. function returning a function object

def createGenerator():
    myList3=range(3)
    for i in myList3:
        yield i*i # this function returns the generator '(i*i for i in range(3))'

myGenerator=createGenerator()
print myGenerator # 'myGenerator' is an initerable 'generator object'
for i in myGenerator:
    print i,
print


#===================================
print

# Controlling a generator exhaustion

#create Bank class, which can create ATMs
class Bank():
    crisis=False
    def create_atm(self):
        while not self.crisis:
            yield "$100"

#when everything's OK, the ATM gives you as much money as you want (each iterative withdrawls yields $100)
bank=Bank()
beforeCrisisATM=bank.create_atm()
print [beforeCrisisATM.next() for i in range(9)]

# Create a crisis, so that new ATM's will not be able to dispense cash
bank.crisis=True
try:
    print beforeCrisisATM.next()
except StopIteration:
    print "beforeCrisisATM threw StopIteration exception!"

# Creating a new ATM won't help, because the bank is still in crisis
duringCrisisATM=bank.create_atm()
try:
    print duringCrisisATM.next()
except StopIteration:
    print "duringCrisisATM threw StopIteration exception!"

# The trouble is, even post-crisis, the ATMs remain empty,
# because once the generator ran out for watever reason
# (e.g. due to an if/else statement such as in the Bank() case)
# there is no place for the iterator to pick up, and the generator is dead.
bank.crisis=False
try:
    print beforeCrisisATM.next()
except StopIteration:
    print "beforeCrisisATM threw StopIteration exception!"
try:
    print duringCrisisATM.next()
except StopIteration:
    print "duringCrisisATM threw StopIteration exception!"

# However, if we now build another ATM, this new one doesn't know about the past crisis
postCrisisATM=bank.create_atm()
print postCrisisATM.next()
print postCrisisATM.next()
print postCrisisATM.next()


#=====================
print

# The itertools module
import itertools

# e.g. possible orders of arrival for a 4 horse race (i.e. all permutations of four items)
horses=[1,2,3,4]
races=itertools.permutations(horses)
print races
print list(races)


#==================
print

# Generator Pattern

class FirstN(object):
    def __init__(self, n):
        self.n=n

    def __iter__(self):
        return self

#sumOfFirstN=sum(FirstN(100))

#===========
print

# Example: Fibonacci sequence (http://stackoverflow.com/questions/3953749/python-fibonacci-generator)

fibSeqLength = int(raw_input("Enter Fibonacci sequence length:"))

# Iteration generation using the yield keyword:
# This implementations do not store the entire sequence, and therefore the memory taken does not scale with 'fibSeqLength'
def fibYield():
    a, b = 0, 1 # base case
    while True:
        yield a # return a generator to iterate 'a'
        a, b = b, a + b # promote values of the next elements in the sequence

a=fibYield() # 'a' is now the object returned by 'fibYield()' -- a generator

for i in range(fibSeqLength): # loop for all elements in input range
    print a.next(), # print the value of the next iteration
print

# Using iteration over list data-structure
# Since this implementation stores the entire sequence to a list, its memory requirement scales with 'fibSeqLength'
def fibList(n):
      a, b = 0, 1
      for i in xrange(n):
          yield a
          a, b = b, a + b

print list(fibList(fibSeqLength))

# Using anaylitical golden ratio expression:

sqrt5=pow(5,0.5)
goldenRatio=(1 + sqrt5)/2

def fibGoldenRatio(n):
    return int( (pow(goldenRatio, n) - pow(1-goldenRatio, n))/sqrt5)

for n in range(fibSeqLength):
    print fibGoldenRatio(n),
print

#===========================================================
print

# Example: Self expanding binary tree search for node values distanced in given range from some reference object ('distance' in this respect is defined elswhere)

# In the following example we will use the extend() keyword:
myList4=['a','b']
myList5=['c','d']
myList4.extend(myList5)
print myList4

print
# Prequisites:
class node(object): # 'node' object class
    _values, _median = 0, 0# some attributes of this node
    _leftchild=None # reference to left child node, if one exists
    _rightchild=None # reference to right child node, if one exists

    def _get_dist(self, obj): # somehow claculates the "distance" between the node and some reference object 'obj'
        pass

    def _get_child_candidates(self, distance, min_dist, max_dist): # 'node' object method returning generators to iterate over children, if there are any (threfore called child candidates)
        if self._leftchild and distance - max_dist < self._median: # if there exists a child on the node's left, and the distance to it is small enough, generate an iterator
            yield self._leftchild
        if self._rightchild and distance + max_dist >= self._median: # equivalent for child on node's right
            yield self._rightchild
	# If the function arrives here, the generator will be considered empty (there are only two children at most -- a binary tree)


# Caller (from within some other function):
result, candidates = list(), [self] # Create an empty list and a list with the current object reference
while candidates: # Loop on children candidates (starting from the head node)
    node = candidates.pop() # Get the last candidate and remove it from the list
    distance = node._get_dist(obj) # Get the distance between the candidate node and some reference object 'obj'
    if distance <= max_dist and distance >= min_dist: # If the candidate node's distance from the reference object is in the range [min_dist:max_dist], add the candidate node values to the result list (uses the 'extend' keyword)
        result.extend(node._values)
    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist)) # extend the list of candidates by executing the generator function above to get the child candidates of the current node. Thus, the loop will keep running until it will have looked at all the children of the children of the children, etc. of the head node
#return result
