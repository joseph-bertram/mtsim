#!/usr/bin/env python3

from mtsim import *

args = {"arg1": 1, "arg2": 2} # arguments to be given

# simple thread to execute 
def example0(x):
    print(x) # prints the argument given to example0
    mt_die() # mt routine to kill a thread

### Test cases for mt_spawn(thread_body, args)
'''
    Stacks the thread onto the runnable stacks while updating the statistics.
'''
def example_spawn(args):
    mt_spawn(example0, args) # thread 1
    mt_spawn(example0, args) # thread 2
    mt_spawn(example0, args) # thread 3
    mt_spawn(example0, args) # thread 4
    mt_die()

### Test cases for mt_run(fcn, args, tid, node, nodes)
'''
    runs the thread on the runnable stack with its corresponding arguments (done by mt_spawn).
    assuming there are 16 nodes on the machine, running from node 0 to node 15.
    assuming the tid starts from 0.
'''
mt_run(example_spawn, args, 0, 0, 16) # runs mt_run with example_spawn as the function to run, args as the arguments, 0 as the starting tid, 0 as the starting node, and 16 for the total nodes. 

### Test cases for mt_array_malloc(variable, map_fcn, map_parameters) in case of mapping by means of mt_block_cyclic(map_parameters, i)
'''
    adds entry to the runtime global dictionary that holds the mapping of example_array_cyclic tomt_block_cyclic.
    parameter [0, 2, 16] means 0 is the first node to receive, 2 blocks of sequential elements to be kept on same node, and 16 total number of nodes to cover.  
'''
example_array_cyclic = list(range(20)) # construct a list of indices from 0 up to 19
mt_array_malloc(example_array_cyclic, mt_block_cyclic, [0, 2, 16]) # runs mt_array_malloc with example_array_cyclic as the array used, mt_block_cyclic as the map function, and [0, 2, 16] as the map parameters.

### Test cases for mt_array_malloc(variable, map_fcn, map_parameters) in case of mapping by means of mt_single(map_parameters)
'''
    adds entry to the runtime global dictionary that holds the mapping of example_array_single to mt_single.
    parameter [3] means all threads are to be assigned on node 3.
'''
example_array_single = list(range(20, 40)) # construct a list of indices from 20 to 39
mt_array_malloc(example_array_single, mt_single, [3]) # runs mt_array_malloc with example_array_single as the array used, mt_single as the map function, and [3] as the map parameter.

### Test cases for mt_block_cyclic(map_parameters, i)
'''
    returns a node upon running mt_block_cylic.
    test cases from index 0 to 9.
    parameter [0, 2, 16] means 0 is the first node to receive, 2 blocks of sequential elements to be kept on same node, and 16 total number of nodes to cover.
'''
print() # prints a new line for aesthetic purpose
print("Block-cylic mapping:")
for i in range(10):
    node = mt_block_cyclic([0, 2, 16], i) # returns a node upon running mt_block_cyclic with [0, 2, 16] as map parameters and i as its index.
    print(f"Component {i} of example_array_cyclic is on node {node}")

### Test cases for mt_single(map_parameters)
'''
    returns a node upon running mt_single.i
    test cases from index 0 to 9.
    parameter [3] means all threads are to be assigned on node 3.
'''
print() # print new line for aesthetic purpose
print("Single-node mapping:")
for i in range(10):
    node = mt_single([3])
    print(f"Component of {i} of example_array_single is on node {node}")

### Test cases for mt_array_read(x, i)
''' 
    testing mt_array_read to read example_array_cyclic (an array).
    only the first 10 elements of example_array_cyclic will be read (from index 0 to 9).
'''
print() # print new line for aesthetic purpose
print("Testing mt_array_read with block-cyclic array:")
for i in range(10):
    value = mt_array_read(example_array_cyclic, i) # returns the value of example_array_cyclic at index i upon running mt_array_read.
    print(f"Value at index {i} is {value}")

'''
    testing mt_array_read to read example_array_single (an array)
    only the first 10 elements of example_array_single will be read (from index 0 to 9).
'''
print() # print new line for aesthetic purpose
print("Testing mt_array_read with single-node array:")
for i in range(10):
    value = mt_array_read(example_array_single, i) # returns the value of example_array_single at index i upon running mt_array_read
    print(f"Value at index {i} is {value}")

### Test cases for summing up all the elements in example_array_cyclic
print() # prints new line for aesthetic purpose
total = 0
for i in range(0, len(example_array_cyclic)):
    total = total + mt_array_read(example_array_cyclic, i)
print(f"The total accumulated in example_array_cyclic is {total}")

### Test cases for summing up all the elements in example_array_single
print() # prints new line for aesthetic purpose
total = 0
for i in range(0, len(example_array_single)):
    total = total + mt_array_read(example_array_single, i)
print(f"The total accumulated in example_array_cyclic is {total}")


    





