#!/usr/bin/env python
"""
Build the Rust library:
  cd pyext-myrustlib && cargo build --release

Copy the library to the root folder for import
  cd ../ && cp pyext-myrustlib/target/release/libmyrustlib.dylib ./myrustlib.so

Run the pytest benchmark
  pytest doubles.py
"""
import re
import string
import random
import itertools
import numpy as np
import myrustlib

# Pure python version
def count_doubles_python(val):
    total = 0
    chars = iter(val)
    c1 = next(chars)
    for c2 in chars:
        if c1 == c2:
            total += 1
        c1 = c2
    return total
    

# Python itertools version
def count_doubles_itertools(val):
    c1s, c2s = itertools.tee(val)
    next(c2s, None)
    total = 0
    for c1, c2 in zip(c1s, c2s):
        if c1 == c2:
            total += 1
    return total
    
    
# List comprehension
def count_doubles_comprehension(val):
    return sum(1 for c1, c2 in zip(val, val[1:]) if c1 == c2)


# Python REGEXP version
double_re = re.compile(r'(?=(.)\1)')
def count_doubles_regex(val):
    return len(double_re.findall(val))
    
# Numpy
def count_double_numpy(val):
    ng=np.frombuffer(val.encode('utf-8'), dtype=np.byte)
    return np.sum(ng[:-1]==ng[1:])


# Benchmark it
# generate 1M random letters for testing
val = ''.join(random.choice(string.ascii_letters) for i in range(1000000))

def test_pure_python(benchmark):
    benchmark(count_doubles_python, val)
    
def test_python_itertools(benchmark):
    benchmark(count_doubles_itertools, val)
    
def test_python_comprehension(benchmark):
    benchmark(count_doubles_comprehension, val)
    
def test_python_numpy(benchmark):
    benchmark(count_double_numpy, val)

def test_regex(benchmark):
    benchmark(count_doubles_regex, val)
    
def test_rust(benchmark):
    benchmark(myrustlib.count_doubles, val)