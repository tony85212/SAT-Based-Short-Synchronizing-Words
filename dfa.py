from pysmt.shortcuts import Symbol, Or, And, Not, Equals, get_model, is_sat, Solver
from pysmt.typing import INT
import string
import random
import sys
import time


class DFA:

    current_state = None

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):

        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        return

    def transition_to_state_with_input(self, input_value):

        if ((self.current_state, input_value) not in self.transition_function.keys()):
            self.current_state = None
            return

        self.current_state = self.transition_function[(self.current_state, input_value)]
        return


    def in_accept_state(self):

        return self.current_state# in accept_states;

    def go_to_initial_state(self):

        self.current_state = self.start_state
        return

    def run_with_input_list(self, input_list):

        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
            continue
        return self.in_accept_state()

def DFA_generator(num_states, num_alphabet):
    states = [i for i in range(num_states)]
    alphabet = list(string.ascii_lowercase[0:num_alphabet])

    tf = dict()
    for i in states:
        for j in alphabet:
            tf[(i, j)] = random.choice(states)

    return DFA(states, alphabet, tf, 0, states)

def output_dfa(d):
    print( len(d.states), len(d.alphabet) )
    for key, value in d.transition_function.items():
        print(key[0], key[1], value)

def enumarate_input(alphabet, c):
    l = []
    def enumarate_recursive(alphabet, str, c):
        if(c == 1):
            for i in alphabet:
                tmp = str + i
                l.append(tmp)
        else:
            for i in alphabet:
                tmp = str + i
                enumarate_recursive(alphabet, tmp, c-1)
    enumarate_recursive(alphabet, '', c)
    return l

def brute_force(d):
    length = 1
    while (length < (len(d.states)-1)**2 + 1):
        all_possible_input = enumarate_input(d.alphabet, length)

        for input in all_possible_input:
            inp_program = list(input)
            #print("input =", input)
            final_state = []
            for initial_state in d.states:
                d.start_state = initial_state
                final_state.append(d.run_with_input_list(inp_program))
            #print(final_state)
            if(len(set(final_state)) == 1):
                return input
        length += 1
    return None

def CNF_gen(d, length):

    alphabet = d.alphabet
    num_alphabet = len(alphabet)
    num_state = len(d.states)

    #constraint 1

    constraint_1 = []

    X = [[Symbol('X' + str(i) + j) for j in alphabet] for i in range(length)]

    for i in range(length):
        constraint_1.append(Or(X[i]))
        for j in range(num_alphabet):
            for k in range(j+1, num_alphabet):
                p = Or(Not(X[i][j]), Not(X[i][k]))
                constraint_1.append(p)
    c1 = And(constraint_1)

    #constraint 2

    constraint_2 = []

    S = [[[Symbol('S' + str(i) + str(j) + str(k)) for k in range(num_state)] for j in range(length+1)] for i in range(num_state)]

    for i in range(num_state):
        for j in range(length+1):
            constraint_2.append(Or(S[i][j]))
            for k in range(num_state):
                for l in range(k+1, num_state):
                    p = Or(Not(S[i][j][k]), Not(S[i][j][l]))
                    constraint_2.append(p)
    c2 = And(constraint_2)

    #constraint 3

    constraint_3 = []
    for i in range(num_state):
        constraint_3.append(S[i][0][i])
    c3 = And(constraint_3)

    #constraint 4

    constraint_4 = []

    for i in range(num_state):
        for j in range(length):
            for k in range(num_state):
                for l in range(num_alphabet):
                    tran_func = (k, alphabet[l])
                    next_state = d.transition_function[tran_func]
                    #print(S[i][j][k], X[j][l], S[i][j+1][next_state])
                    p = Or(Not(S[i][j][k]), Not(X[j][l]), S[i][j+1][next_state])
                    constraint_4.append(p)

    c4 = And(constraint_4)

    #constraint 5

    constraint_5 = []
    Y = [Symbol('Y'+ str(i)) for i in range(num_state)]
    constraint_5.append(Or(Y))

    for i in range(num_state):
    	for j in range(i+1, num_state):
    		p = Or(Not(Y[i]), Not(Y[j]))
    		constraint_5.append(p)

    c5 = And(constraint_5)

    #constraint 6
    constraint_6 = []
    for i in range(num_state):
        for j in range(num_state):
            p = Or(Not(Y[i]), S[j][length][i])
            constraint_6.append(p)

    c6 = And(constraint_6)

    CNF = And(c1, c2, c3, c4, c5, c6)

    model = get_model(CNF)
    synchronizing_words = []
    if(not model):
        #print("not Satisfied")
        pass
    else:
        for i in range(length):
            for j in range(num_alphabet):
                #print(str(model[X[i][j]]))
                if(str(model[X[i][j]]) == 'True'):
                    synchronizing_words.append(alphabet[j])
        return ''.join(synchronizing_words)
    return None

def SAT_based(d):
    solution = None
    for i in range(1, (len(d.states)-1)**2 + 1):
        solution = CNF_gen(d, i)
        if(solution != None):
            break

    return solution

def main():
    #read dfa from input
    l = []
    for line in sys.stdin:
        l.append(line.strip().split(' '))

    num_state = int(l[0][0])
    num_alphabet = int(l[0][1])

    states = [i for i in range(num_state)]
    alphabet = list(string.ascii_lowercase[0:num_alphabet])

    tf = dict();

    for i in range(1, len(l)):
        tran_func = (int(l[i][0]), l[i][1])
        tf[tran_func] = int(l[i][2])

    d = DFA_generator(20, 2)
    #d = DFA(states, alphabet, tf, 0, states)

    time0 = time.time()
    pp = SAT_based(d)
    time1 = time.time()
    print(pp, time1 - time0)

    time0 = time.time()
    aa = brute_force(d)
    time1 = time.time()
    print(aa, time1 - time0)

if __name__== "__main__":
  main()
