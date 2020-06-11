# SAT-Based-Short-Synchronizing-Words


## Prerequisites:

 Make sure install python3 and pysmt
 https://github.com/pysmt/pysmt/blob/bc3a5f8ae22c490016a4ce98df10b7f79ac40324/README.rst

 Note: The defualt SAT-solver is z3. (solver also need to be download to path)

## Running Instrction:

 --input version:

  > python synchronizing_words.py --input < DFA/dfa1.txt
  
 --random version:

  > python synchronizing_words.py --random 6 2            **(n states, k inputs)**
 
 --eval version:

  > python synchronizing_words.py --eval < DFA/dfa1.txt
  
  
