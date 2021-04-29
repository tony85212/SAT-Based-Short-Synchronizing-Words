# SAT-Based-Short-Synchronizing-Words

## Introduction

In the past research, determine a given DFA, whether it has a synchronizing word can be done
in polynomial time. From the other side, finding the shortest synchronizing word is NP-Hard.
Although there exist some algorithms in polynomial time with less states or binary input
alphabet, the problem becomes more complex with more states and input alphabet.

For this problem, brute-force is a straightful algorithm which enumerates all the possible
synchronizing words and finding the shortest one. Boolean Satisfiability Problem (SAT) solvers
can be assumed as a smart brute-force search, since SAT solvers can find smart solutions to
SAT problems. In the project, it will calculate the results in the case of SAT-based.

![Scree]()

## Prerequisites

 Make sure install python3 and pysmt
 https://github.com/pysmt/pysmt/blob/bc3a5f8ae22c490016a4ce98df10b7f79ac40324/README.rst

 Note: The defualt SAT-solver is z3. (solver also need to be download to path)

## Running Instrction

 --input version:

  > python synchronizing_words.py --input < DFA/dfa1.txt
  
 --random version:

  > python synchronizing_words.py --random 6 2            **(n states, k inputs)**
 
 --eval version:

  > python synchronizing_words.py --eval < DFA/dfa1.txt
  
  
