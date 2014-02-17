#! /usr/bin/python

# In Python, and other languages, functions are "first class citizens":
# They are objects which can be treated as you would a variable or any other object 
# (passed as argument to another function, returned by a function, and so on). 
#
# A function which takes or returns a function is called a functional, or higher-order function 
# (e.g. an integral takes a function as an argument). 
#
# Use of these properties is called the functional programming paradigm.
#
# The origin for (and simplest instance of) a functional object is the labmda expression.

#http://docs.python.org/release/2.7.6/tutorial/

#==============================================

# 4.7.5 Lambda expressions (c.f. C function pointers)
# "Lambda expression" here is a small, anonymous function;
# used whenever a function is required to be represented as an object.
# Syntactically restricted to a single expression...

# Lambda expression returning unevaluated function object
add = lambda a,b: a+b
print add(1,2) # evaluate function object
argsList=[2,3]
print apply(add,argsList) # using non-essential 'apply()' function

# Lambda expresssion referrencing value from containing scope (like nested function definitions)
def make_incrementor(n):
    return lambda x: x+n # given parameter 'n' and taking argument 'x', return the value 'x+n'
f=make_incrementor(42) # 'f' is now a function object with n=42
print "f(0)= ", f(0) # print the evaluated function for x=0
print "f(1)= ", f(1) # print the evaluated function for x=1

# Sort list according to a key, where the key is a lambda expression
pairs=[(1,'one'),(2,'two'),(3,'three'),(4,'four')]
print "Before sort: ", pairs
pairKey=lambda pair: pair[1] # Lambda expression which, given an object 'pair', returns the [1] element (i.e. the second elemnt in the tuple)
pairs.sort(key=pairKey) # Sort pairs according to the name of the number (i.e. alphabetically)
print "After sort: ", pairs

#==============================================
print

# 5.1.3 Functional programming (functional = higher-order function)

# Filter (aka C++ <algorithm> remove_copy_if() , etc.)

# Example: filter out Capital letters, punctuation marks, and spaces
stringEx="Hello World!"
print stringEx
def someBoolFunction(x):
    return (ord(x) > 97) # is the ASCII value of the character x greater than 97?
print filter(someBoolFunction,stringEx) # returns only string, tuple or list (depending on input)

# Example: compute a sequence of numbers not divisible by 2 or 3
def notDiv2or3(x):
    return (0 != x % 2) and (0 != x % 3)
print filter(notDiv2or3, range(2,25)) # recall that range is inclusive of 'from' argument and exclusive of 'to' argument

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print

# Map (aka C++ <algorithm> transform()

# Example: "do for each" return cube
def cube(x):
    return x*x*x
print map(cube, range(1,10))

# Example: map multiple sequences (e.g. lists)
def add2(a,b):
##    if int(a) and int(b): return a+b
##    elif int(a): return a                 # i.e. ! int(b)
##    else: return b                        #  int(b) but ! int(a)
##    if (type(a) is IntType) and (type(b) is IntType): return a+b # requires 'from types import *'
    return a+b if (type(a)== type(b)) else 'undefined'
seq1=range(0,8)
seq2=range(-6,4) # note that len(seq2) > len(seq1)
print map(add2,seq1,seq2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print

# Reduce (aka Fold, C++ <numeric> accumulate()
# see also python 3 'compose' and Haskell 'scan'

# serial composition of binary function (takes two arguments at a time) from left to right:

# leftFold(f;a,b,c,d)  = f( f( f(a,b) ,c) ,d)
print "((2/3)/4)/5 = 1/30",
def div(x,y): return float(x)/float(y)
l=range(2,6)
print reduce(div,l)

# can take initial value argument:
print "((((1)/2)/3)/4)/5 = 1/120",
initVal=1
print reduce(div,l,initVal)

# rightFold(f;a,b,c,d) = f(a , f(b, f(c,d) ) )
print "2/(3/(4/5)) = 8/15",
def vid(x,y):
    return div(y,x) # reverse function object
lRev=reversed(range(2,6)) # reverse argument list (compose d,c, then b, then a ...)
print reduce(vid,lRev)

# Example: sum numbers from 1 through 10 (inclusive)
def add(x,y): return x+y
print reduce(add,range(1,11))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print

# Example: Parralelization of search for all multiples of 'q' in the range [a:b]
# 1) Split range [a:b] to n sub-ranges.
# 2) MAP multiple-finding function to each sub-range, and execute in parallel.
# 3) REDUCE result lists back to a single list.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print

# Creating a list using functional programming
# specifically, using map()...

squaresLambda=map(lambda x: x**2, range(3))
print squaresLambda


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print
# 5.1.4 listcomp: List comprehension
# Concise way of creating a list in which each element is the result of some opperation, applied to each member of another sequence or iterable.

squaresExplicit=[] # create empty list
for x in range(3):
    squaresExplicit.append(x**2)
print squaresExplicit

squaresListcomp=[x**2 for x in range(3)] #concise expression, using list compehension
print squaresListcomp


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print
# More complex list comprehension (more than one 'for' and additional 'if' clauses)
# For example, the sequence of subsequences of non-negative integers,
# such that each subsequence is shorter than 6 integers long (including zero)
seqOfsubSeq=[x for y in range(10) for x in range(y) if y<6]
print seqOfsubSeq
