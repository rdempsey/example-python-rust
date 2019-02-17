# Python Rust Example
Example application showing the integration of Python and Rust with a *very* simplistic benchmark.

## Introduction

One of the biggest complaints when I started using Ruby on Rails (in 2008) was it was slow. To speed it up, one could [create a C extension](http://www.rubyinside.com/how-to-create-a-ruby-extension-in-c-in-43-seconds-167.html). Today, I hear the same complaints being lodged against my go-to language, Python. Do we need to learn C?

While "fast" is relative to the application and horizontal scaling is easy when deploying to cloud platforms, there are times when seconds, even milliseconds, matter.

If you've hit a wall optimizing your Python code, it may be time to go lower level. And for that, [Rust](https://www.rust-lang.org/) is a solid option.

I've been reading about Rust for a while and wanted to see how to use it with Python. For that, I turned to Google, and found the article, [Speed up your Python using Rust](https://developers.redhat.com/blog/2017/11/16/speed-python-using-rust/) by Bruno Rocha.

I won't repeat the excellent article here as I suggest you read it, however I updated some of the code to work with [Python](https://www.python.org/) 3.7.2, [Numpy](http://www.numpy.org/) 1.6.1, [Rust](https://www.rust-lang.org/) 1.32.0, [rust-cpython](https://github.com/dgrunwald/rust-cpython) 0.2, and [pytest-benchmark](https://github.com/ionelmc/pytest-benchmark/).

## Running the Code (On Mac/Linux)

To test this out on your Mac do the following:

1. Clone this repo and cd into the directory.
2. Install Python 3.7.x, create a new virtual environment, and install the requirements.
3. Install Rust.
4. Change into the `pyext-myrustlib` directory and build the library: `cargo build --release`
5. Change back into the root directory
6. Copy the new library into the root directory and change it to a `.so` file for use: `cp pyext-myrustlib/target/release/libmyrustlib.dylib ./myrustlib.so`
7. Run the benchmarks: `pytest doubles.py`

## How Much Faster is Rust Than Pure Python?

Let's take a look...

For the simple benchmark we're using a function that counts pairs of repeated characters in a string of 1 million random characters (sounds like an interview problem...).

Now there are a few ways to parse that string, so we'll use the following:

1. Pure Python
2. [Itertools](https://docs.python.org/3.7/library/itertools.html)
3. [List comprehension](https://www.pythonforbeginners.com/basics/list-comprehensions-in-python)
4. Numpy
5. [Regex](https://docs.python.org/3.7/library/re.html)
6. Rust

Here's how they perform on my MacBook Pro: macOS Mojave, 2.2 GHz Intel Core i7, 16 GB RAM:

| Name (time in us)         | Min                  | Max                 | Mean                 |
| ------------------------- | -------------------- | ------------------- | -------------------- |
| test_rust                 | 440.6270 (1.0)       | 926.0550 (1.0)      | 486.1527 (1.0)       |
| test_python_numpy         | 1,105.9690 (2.51)    | 2,461.2190 (2.66)   | 1,221.5940 (2.51)    |
| test_regex                | 26,473.0460 (60.08)  | 34,816.4480 (37.60) | 27,283.4936 (56.12)  |
| test_pure_python          | 42,791.8280 (97.12)  | 45,206.2730 (48.82) | 43,268.9481 (89.00)  |
| test_python_comprehension | 55,309.7680 (125.53) | 59,225.5910 (63.95) | 56,470.0048 (116.16) |
| test_python_itertools     | 63,602.1140 (144.34) | 76,422.4370 (82.52) | 66,260.3507 (136.30) |

**Result**: Using Mean as the comparision, Rust beats pure Python *in this one instance* by a lot: it's 56x faster than Python regex, and 89x faster than pure Python. However, it's only 2.5x faster than numpy!

This also shows that while a list comprehension is easier to read, it's not the best implementation for this example.

## Conclusion

Using Rust to speed up specific parts of your Python application can be a great and relatively easy way to go. Try out rust-cpython for yourself, or another available option (which I will be trying soon), [PyO3](https://github.com/PyO3/pyo3).